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

from arch.api.table.pyspark import materialize
from arch.api.table.pyspark.cluster.rddtable import RDDTable
from arch.api.table.table_manager import TableManager


# noinspection PyProtectedMember
class RDDTableManager(TableManager):
    """
    manage RDDTable, use EggRoleStorage as storage
    """

    def __init__(self, job_id, eggroll_context, server_conf_path="arch/conf/server_conf.json"):
        from arch.api.table.eggroll.cluster.table_manager import EggRollTableManager
        self.eggroll_table_manager = EggRollTableManager(job_id=job_id,
                                                         server_conf_path=server_conf_path,
                                                         eggroll_context=eggroll_context)

        # init PySpark
        conf = SparkConf().setAppName("FATE-PySpark-{job_id}".format(job_id=job_id))
        sc = SparkContext.getOrCreate(conf)
        self.sc = sc
        self.job_id = job_id

    def table(self,
              name,
              namespace,
              partition=1,
              create_if_missing=True,
              error_if_exist=False,
              persistent=True,
              in_place_computing=False):
        dtable = self.eggroll_table_manager.table(name=name, namespace=namespace, partition=partition,
                                                  create_if_missing=create_if_missing, error_if_exist=error_if_exist,
                                                  persistent=persistent, in_place_computing=in_place_computing)
        return RDDTable(eggroll_table=dtable, partitions=dtable.partitions())

    def parallelize(self,
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

    def cleanup(self, name, namespace, persistent=False):
        self.eggroll_table_manager.cleanup(name=name, namespace=namespace, persistent=persistent)

    def generateUniqueId(self):
        self.eggroll_table_manager.generateUniqueId()

    def get_job_id(self):
        return self.job_id
