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

from arch.api import RuntimeInstance, WorkMode


def init_federation(job_id, runtime_conf, server_conf_path="arch/conf/server_conf.json"):
    if RuntimeInstance.MODE is None:
        raise EnvironmentError("eggroll should be initialized before federation")
    if RuntimeInstance.MODE == WorkMode.STANDALONE:
        from arch.api.table.eggroll.standalone.federation import FederationRuntime
        federation = FederationRuntime(job_id=job_id, runtime_conf=runtime_conf)

    elif RuntimeInstance.MODE == WorkMode.CLUSTER:
        from arch.api.table.eggroll.cluster.federation import FederationRuntime
        federation = FederationRuntime(job_id=job_id, runtime_conf=runtime_conf,
                                       server_conf_path=server_conf_path)

    elif RuntimeInstance.MODE == WorkMode.STANDALONE_SPARK:
        from arch.api.table.pyspark.standalone.federation import FederationRuntime
        federation = FederationRuntime(job_id=job_id, runtime_conf=runtime_conf)

    else:
        from arch.api.table.pyspark.cluster.federation import FederationRuntime
        federation = FederationRuntime(job_id=job_id, runtime_conf=runtime_conf,
                                       server_conf_path=server_conf_path)

    RuntimeInstance.FEDERATION = federation
