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
import threading
import uuid
from typing import Iterable

import six

from arch.api import RuntimeInstance
from arch.api import WorkMode, NamingPolicy
from arch.api.table.table import Table
from arch.api.utils import file_utils
from arch.api.utils.log_utils import LoggerFactory


def init(job_id, mode: WorkMode, naming_policy: NamingPolicy):
    if RuntimeInstance.TABLE_MANAGER:
        return

    if job_id is None:
        job_id = str(uuid.uuid1())
        LoggerFactory.setDirectory()
    else:
        LoggerFactory.setDirectory(os.path.join(file_utils.get_project_base_directory(), 'logs', job_id))

    RuntimeInstance.MODE = mode

    if mode == WorkMode.STANDALONE or mode == WorkMode.CLUSTER:
        from arch.api.table.eggroll.table_manager import EggRoleTableManager
        eggroll_manager = EggRoleTableManager(job_id=job_id, mode=mode, naming_policy=naming_policy)
        RuntimeInstance.TABLE_MANAGER = eggroll_manager
        TableManager.set_instance(eggroll_manager)

    elif mode == WorkMode.STANDALONE_SPARK or mode == WorkMode.CLUSTER_SPARK:
        from arch.api.table.pyspark.table_manager import RDDTableManager
        rdd_manager = RDDTableManager(job_id=job_id, mode=mode, naming_policy=naming_policy)
        RuntimeInstance.TABLE_MANAGER = rdd_manager
        TableManager.set_instance(rdd_manager)


@six.add_metaclass(abc.ABCMeta)
class TableManager(object):
    _instance_lock = threading.Lock()
    _instance = None

    @abc.abstractmethod
    def _table(self,
               name,
               namespace,
               partition=1,
               create_if_missing=True,
               error_if_exist=False,
               persistent=True,
               in_place_computing=False) -> Table:
        pass

    @abc.abstractmethod
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
                     in_place_computing=False) -> Table:
        pass

    @abc.abstractmethod
    def _cleanup(self, name, namespace, persistent=False):
        pass

    # noinspection PyPep8Naming
    @abc.abstractmethod
    def _generateUniqueId(self):
        pass

    @abc.abstractmethod
    def _get_job_id(self):
        pass

    @staticmethod
    def set_instance(inst):
        if TableManager._instance is None:
            with TableManager._instance_lock:
                if TableManager._instance is None:
                    TableManager._instance = inst
        else:
            pass  # todo: add warning log

    @staticmethod
    def get_instance() -> 'TableManager':
        if TableManager._instance is None:
            raise EnvironmentError("table manager should initialize before use")
        return TableManager._instance

    @staticmethod
    def table(name,
              namespace,
              partition=1,
              create_if_missing=True,
              error_if_exist=False,
              persistent=True,
              in_place_computing=False) -> Table:

        return TableManager.get_instance()\
            ._table(name=name, namespace=namespace, partition=partition,
                    create_if_missing=create_if_missing, error_if_exist=error_if_exist,
                    persistent=persistent, in_place_computing=in_place_computing)

    @staticmethod
    def parallelize(data: Iterable,
                    include_key=False,
                    name=None,
                    partition=1,
                    namespace=None,
                    create_if_missing=True,
                    error_if_exist=False,
                    persistent=False,
                    chunk_size=100000,
                    in_place_computing=False) -> Table:
        return TableManager.get_instance()\
            ._parallelize(data=data, include_key=include_key, name=name, partition=partition, namespace=namespace,
                          create_if_missing=create_if_missing, error_if_exist=error_if_exist,
                          persistent=persistent, chunk_size=chunk_size, in_place_computing=in_place_computing)

    @staticmethod
    def cleanup(name, namespace, persistent):
        return TableManager.get_instance()\
            ._cleanup(name=name, namespace=namespace, persistent=persistent)

    # noinspection PyPep8Naming
    @staticmethod
    def generateUniqueId():
        return TableManager.get_instance()._generateUniqueId()

    @staticmethod
    def get_job_id():
        return TableManager.get_instance()._get_job_id()
