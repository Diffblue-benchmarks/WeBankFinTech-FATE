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

from arch.api import WorkMode
from arch.api.table.eggroll.storage import EggRollStorage
from arch.api.table.pyspark.rddtable import RDDTable


class FederationRuntime(object):
    instance = None

    def __init__(self, eggroll_federation, mode: WorkMode = WorkMode.STANDALONE_SPARK):
        if mode == WorkMode.STANDALONE_SPARK or mode == WorkMode.CLUSTER_SPARK:
            self.eggroll_federation = eggroll_federation
            FederationRuntime.instance = self
            self.mode = mode
        else:
            raise AssertionError("mode should be CLUSTER_SPARK or STANDALONE_SPARK")

    @staticmethod
    def get_instance():
        if FederationRuntime.instance is None:
            raise EnvironmentError("federation should be initialized before use")
        return FederationRuntime.instance

    # noinspection PyProtectedMember
    def _get_standalone(self, name, tag, idx):
        from arch.api.standalone.eggroll import _DTable
        ret = self.eggroll_federation.get(name=name, tag=tag, idx=idx)
        if isinstance(ret, _DTable):
            ret = RDDTable(storage=EggRollStorage(ret))
        return ret

    # noinspection PyProtectedMember
    def _get_cluster(self, name, tag, idx):
        from arch.api.cluster.eggroll import _DTable
        ret = self.eggroll_federation.get(name=name, tag=tag, idx=idx)
        if isinstance(ret, _DTable):
            ret = RDDTable(storage=EggRollStorage(ret))
        return ret

    def get(self, name, tag, idx=-1):
        if self.mode == WorkMode.STANDALONE_SPARK:
            return self._get_standalone(name, tag, idx)
        else:
            return self._get_cluster(name, tag, idx)

    def remote(self, obj, name: str, tag: str, role=None, idx=-1):
        if isinstance(obj, RDDTable):
            obj = obj.for_remote()
        return self.eggroll_federation.remote(obj=obj, name=name, tag=tag, role=role, idx=idx)
