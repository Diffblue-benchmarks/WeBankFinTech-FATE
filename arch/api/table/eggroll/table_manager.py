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

from arch.api import RuntimeInstance
from arch.api import WorkMode, NamingPolicy
from arch.api.core import EggRollContext
from arch.api.table.table_manager import TableManager as TableManger


class EggRoleTableManager(TableManger):
    """
    manage _DTable, from EggRole
    """
    def __init__(self, job_id, mode: WorkMode, naming_policy: NamingPolicy):
        if RuntimeInstance.EGGROLL:
            return

        eggroll_context = EggRollContext(naming_policy=naming_policy)
        if mode == WorkMode.STANDALONE or mode == WorkMode.STANDALONE_SPARK:
            from arch.api.standalone.eggroll import Standalone
            RuntimeInstance.EGGROLL = Standalone(job_id=job_id, eggroll_context=eggroll_context)
        elif mode == WorkMode.CLUSTER or mode == WorkMode.CLUSTER_SPARK:
            # noinspection PyProtectedMember
            from arch.api.cluster.eggroll import _EggRoll
            from arch.api.cluster.eggroll import init as c_init
            c_init(job_id, eggroll_context=eggroll_context)
            RuntimeInstance.EGGROLL = _EggRoll.get_instance()
        else:
            from arch.api.cluster import simple_roll
            simple_roll.init(job_id)
            RuntimeInstance.EGGROLL = simple_roll.EggRoll.get_instance()

    """
    implement abc methods
    """

    def _table(self,
               name,
               namespace,
               partition=1,
               create_if_missing=True,
               error_if_exist=False,
               persistent=True,
               in_place_computing=False):
        return RuntimeInstance.EGGROLL.table(name=name, namespace=namespace, partition=partition,
                                             create_if_missing=create_if_missing, error_if_exist=error_if_exist,
                                             persistent=persistent, in_place_computing=in_place_computing)

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
        return RuntimeInstance.EGGROLL.parallelize(data=data, include_key=include_key, name=name, partition=partition,
                                                   namespace=namespace, create_if_missing=create_if_missing,
                                                   error_if_exist=error_if_exist, persistent=persistent,
                                                   chunk_size=chunk_size, in_place_computing=in_place_computing)

    def _cleanup(self, name, namespace, persistent=False):
        return RuntimeInstance.EGGROLL.cleanup(name=name, namespace=namespace, persistent=persistent)

    def _get_job_id(self):
        return RuntimeInstance.EGGROLL.job_id

    def _generateUniqueId(self):
        return RuntimeInstance.EGGROLL.generateUniqueId()
