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

from arch.api.standalone.eggroll import Standalone
from arch.api.table.eggroll.standalone import _make_serializable
from arch.api.table.eggroll.standalone.eggroletable import EggRollTable
from arch.api.table.table_manager import TableManager


class EggRollTableManager(TableManager):
    """
    wrapper of :class:`arch.api.standalone.eggroll.Standalone`
    """

    def __init__(self, job_id=None, eggroll_context=None):
        self._eggroll = Standalone(job_id=job_id, eggroll_context=eggroll_context)
        self._eggroll = _make_serializable(self._eggroll)

    def table(self,
              name,
              namespace,
              partition=1,
              create_if_missing=True,
              error_if_exist=False,
              persistent=True,
              in_place_computing=False) -> EggRollTable:
        d_table = self._eggroll.table(name=name, namespace=namespace, partition=partition,
                                      create_if_missing=create_if_missing, error_if_exist=error_if_exist,
                                      persistent=persistent, in_place_computing=in_place_computing)
        return EggRollTable(d_table)

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
                    in_place_computing=False) -> EggRollTable:
        d_table = self._eggroll.parallelize(data=data, include_key=include_key, name=name, partition=partition,
                                            namespace=namespace, create_if_missing=create_if_missing,
                                            error_if_exist=error_if_exist, persistent=persistent,
                                            chunk_size=chunk_size, in_place_computing=in_place_computing)
        return EggRollTable(d_table)

    def cleanup(self, name, namespace, persistent=False):
        return self._eggroll.cleanup(name=name, namespace=namespace, persistent=persistent)

    # noinspection PyPep8Naming
    def generateUniqueId(self):
        return self._eggroll.generateUniqueId()

    def get_job_id(self):
        return self._eggroll.job_id
