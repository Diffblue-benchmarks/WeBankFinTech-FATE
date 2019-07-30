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

from arch.api.table.eggroll.cluster.eggroletable import EggRollTable
from arch.api.table.eggroll.cluster.federation import FederationRuntime as ClusterFederation
from arch.api.table.pyspark.cluster.rddtable import RDDTable


class FederationRuntime(object):

    def __init__(self, job_id, runtime_conf, server_conf_path):
        self._eggroll_federation = ClusterFederation(job_id, runtime_conf, server_conf_path)

    def _get_all(self, name, tag):
        # noinspection PyProtectedMember
        rtn = self._eggroll_federation._get_all(name, tag)
        if len(rtn) > 0 and isinstance(rtn[0], EggRollTable):
            return [RDDTable(v) for v in rtn]
        else:
            return rtn

    def _get_single(self, name, tag, idx):
        # noinspection PyProtectedMember
        rtn = self._eggroll_federation._get_single(name, tag, idx)
        if isinstance(rtn, EggRollTable):
            return RDDTable(rtn)
        else:
            return rtn

    def get(self, name, tag, idx):
        # noinspection PyProtectedMember
        if self._eggroll_federation._idx_in_range(name, idx):
            return self._get_single(name, tag, idx)
        else:
            return self._get_all(name, tag)

    def remote(self, obj, name: str, tag: str, role=None, idx=-1):
        if isinstance(obj, RDDTable):
            obj = obj.for_remote()
        return self._eggroll_federation.remote(obj=obj, name=name, tag=tag, role=role, idx=idx)
