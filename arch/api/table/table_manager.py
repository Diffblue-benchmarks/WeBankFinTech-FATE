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

import abc
import os
import uuid
from typing import Iterable

import six

from arch.api import WorkMode, NamingPolicy
from arch.api.core import EggRollContext
from arch.api.table.table import Table
from arch.api.utils import file_utils
from arch.api.utils.log_utils import LoggerFactory


def init(job_id, mode: WorkMode, naming_policy: NamingPolicy):
    from arch.api import RuntimeInstance
    if RuntimeInstance.TABLE_MANAGER:
        return

    if job_id is None:
        job_id = str(uuid.uuid1())
        LoggerFactory.setDirectory()
    else:
        LoggerFactory.setDirectory(os.path.join(file_utils.get_project_base_directory(), 'logs', job_id))

    RuntimeInstance.MODE = mode
    eggroll_context = EggRollContext(naming_policy=naming_policy)

    if mode == WorkMode.STANDALONE:
        from arch.api.table.eggroll.standalone.table_manager import EggRollTableManager
        eggroll_manager = EggRollTableManager(job_id=job_id, eggroll_context=eggroll_context)
        RuntimeInstance.TABLE_MANAGER = eggroll_manager
    elif mode == WorkMode.CLUSTER:
        from arch.api.table.eggroll.cluster.table_manager import EggRollTableManager
        eggroll_manager = EggRollTableManager(job_id=job_id, eggroll_context=eggroll_context)
        RuntimeInstance.TABLE_MANAGER = eggroll_manager
    elif mode == WorkMode.STANDALONE_SPARK:
        from arch.api.table.pyspark.standalone.table_manager import RDDTableManager
        rdd_manager = RDDTableManager(job_id=job_id, eggroll_context=eggroll_context)
        RuntimeInstance.TABLE_MANAGER = rdd_manager
    elif mode == WorkMode.CLUSTER_SPARK:
        from arch.api.table.pyspark.cluster.table_manager import RDDTableManager
        rdd_manager = RDDTableManager(job_id=job_id, eggroll_context=eggroll_context)
        RuntimeInstance.TABLE_MANAGER = rdd_manager
    else:
        raise NotImplementedError("mode={mode} is not supported".format(mode=mode))


@six.add_metaclass(abc.ABCMeta)
class TableManager(object):

    @abc.abstractmethod
    def table(self,
              name,
              namespace,
              partition=1,
              create_if_missing=True,
              error_if_exist=False,
              persistent=True,
              in_place_computing=False) -> Table:
        pass

    @abc.abstractmethod
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
                    in_place_computing=False) -> Table:
        pass

    @abc.abstractmethod
    def cleanup(self, name, namespace, persistent=False):
        pass

    # noinspection PyPep8Naming
    @abc.abstractmethod
    def generateUniqueId(self):
        pass

    @abc.abstractmethod
    def get_job_id(self):
        pass
