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
from arch.api import WorkMode, NamingPolicy
from arch.api import RuntimeInstance


def init(job_id=None, mode: WorkMode = WorkMode.STANDALONE, naming_policy: NamingPolicy = NamingPolicy.DEFAULT):
    from arch.api.table.table_manager import init
    init(job_id=job_id, mode=mode, naming_policy=naming_policy)


def table(name, namespace,
          partition=1,
          persistent=True,
          create_if_missing=True,
          error_if_exist=False,
          in_place_computing=False):
    return RuntimeInstance.TABLE_MANAGER.table(name=name, namespace=namespace, partition=partition,
                                               persistent=persistent, in_place_computing=in_place_computing,
                                               create_if_missing=create_if_missing, error_if_exist=error_if_exist)


def parallelize(data: Iterable,
                include_key=False,
                name=None,
                partition=1,
                namespace=None,
                persistent=False,
                create_if_missing=True,
                error_if_exist=False,
                chunk_size=100000,
                in_place_computing=False):
    return RuntimeInstance.TABLE_MANAGER.parallelize(
        data=data, include_key=include_key, name=name, partition=partition,
        namespace=namespace, persistent=persistent, chunk_size=chunk_size,
        in_place_computing=in_place_computing, create_if_missing=create_if_missing, error_if_exist=error_if_exist)


def cleanup(name, namespace, persistent=False):
    return RuntimeInstance.TABLE_MANAGER.cleanup(name=name, namespace=namespace, persistent=persistent)


# noinspection PyPep8Naming
def generateUniqueId():
    return RuntimeInstance.TABLE_MANAGER.generateUniqueId()


def get_job_id():
    return RuntimeInstance.TABLE_MANAGER.get_job_id()
