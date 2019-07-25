#
#  Copyright 2019 The FATE Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

from typing import Iterable

from pyspark import SparkContext, SparkConf

from arch.api import WorkMode, NamingPolicy
from arch.api.table.eggroll.storage import EggRollStorage
from arch.api.table.eggroll.table_manager import EggRoleTableManager
from arch.api.table.pyspark import materialize
from arch.api.table.pyspark.rddtable import RDDTable
from arch.api.table.table_manager import TableManager as TableManger


# noinspection PyProtectedMember
class RDDTableManager(TableManger):
    """
    manage RDDTable, use EggRoleStorage as storage
    """

    def __init__(self, job_id, mode: WorkMode, naming_policy: NamingPolicy):

        # init eggroll
        self.storage_table_manager = \
            EggRoleTableManager(job_id=job_id, mode=mode, naming_policy=naming_policy)

        # init pyspark
        conf = SparkConf().setAppName("FATE-{0}".format(job_id))
        sc = SparkContext.getOrCreate(conf)
        self.sc = sc
        self.job_id = job_id

    def _table(self,
               name,
               namespace,
               partition=1,
               create_if_missing=True,
               error_if_exist=False,
               persistent=True,
               in_place_computing=False):
        dtable = self.storage_table_manager._table(name=name, namespace=namespace, partition=partition,
                                                   create_if_missing=create_if_missing, error_if_exist=error_if_exist,
                                                   persistent=persistent, in_place_computing=in_place_computing)
        # noinspection PyTypeChecker
        _storage = EggRollStorage(dtable)
        return RDDTable(storage=_storage, partitions=_storage.partitions())

    def _parallelize(self,
                     data: Iterable,
                     include_key=False,
                     name=None,
                     partition=1,
                     namespace=None,
                     create_if_missing=True,
                     error_if_exist=False,
                     persistent=False,
                     chunk_size=100000,
                     in_place_computing=False):

        _iter = data if include_key else enumerate(data)
        rdd = self.sc.parallelize(_iter, partition)
        rdd = materialize(rdd)
        rdd_inst = RDDTable(rdd=rdd, partitions=partition)

        return rdd_inst

    def _cleanup(self, name, namespace, persistent=False):
        self.storage_table_manager._cleanup(name=name, namespace=namespace, persistent=persistent)

    def _generateUniqueId(self):
        self.storage_table_manager._generateUniqueId()

    def _get_job_id(self):
        return self.job_id
