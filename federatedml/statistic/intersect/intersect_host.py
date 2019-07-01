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

import hashlib
from arch.api.federation import remote, get
from arch.api.utils import log_utils
from fate_flow.entity.metric import Metric
from federatedml.model_base import ModelBase
from federatedml.param import IntersectParam
from federatedml.secureprotol import gmpy_math
from federatedml.secureprotol.encrypt import RsaEncrypt
from federatedml.statistic.intersect import RawIntersect
from federatedml.statistic.intersect import RsaIntersect
from federatedml.util import consts
from federatedml.util.transfer_variable import RsaIntersectTransferVariable

LOGGER = log_utils.getLogger()


class RsaIntersectionHost(RsaIntersect):
    def __init__(self, intersect_params):
        super().__init__(intersect_params)

        self.get_intersect_ids_flag = intersect_params.is_get_intersect_ids
        self.transfer_variable = RsaIntersectTransferVariable()

        self.e = None
        self.d = None
        self.n = None

    @staticmethod
    def hash(value):
        return hashlib.sha256(bytes(str(value), encoding='utf-8')).hexdigest()

    def run(self, data_instances):
        LOGGER.info("Start rsa intersection")

        encrypt_operator = RsaEncrypt()
        encrypt_operator.generate_key(rsa_bit=1024)
        self.e, self.d, self.n = encrypt_operator.get_key_pair()
        LOGGER.info("Generate rsa keys.")
        public_key = {"e": self.e, "n": self.n}
        remote(public_key,
               name=self.transfer_variable.rsa_pubkey.name,
               tag=self.transfer_variable.generate_transferid(self.transfer_variable.rsa_pubkey),
               role=consts.GUEST,
               idx=0)
        LOGGER.info("Remote public key to Guest.")

        # (host_id_process, 1)
        host_ids_process_pair = data_instances.map(
            lambda k, v: (
                RsaIntersectionHost.hash(gmpy_math.powmod(int(RsaIntersectionHost.hash(k), 16), self.d, self.n)), k)
        )

        host_ids_process = host_ids_process_pair.mapValues(lambda v: 1)
        remote(host_ids_process,
               name=self.transfer_variable.intersect_host_ids_process.name,
               tag=self.transfer_variable.generate_transferid(self.transfer_variable.intersect_host_ids_process),
               role=consts.GUEST,
               idx=0)
        LOGGER.info("Remote host_ids_process to Guest.")

        # Recv guest ids
        guest_ids = get(name=self.transfer_variable.intersect_guest_ids.name,
                        tag=self.transfer_variable.generate_transferid(self.transfer_variable.intersect_guest_ids),
                        idx=0)
        LOGGER.info("Get guest_ids from guest")

        # Process guest ids and return to guest
        guest_ids_process = guest_ids.map(lambda k, v: (k, gmpy_math.powmod(int(k), self.d, self.n)))
        remote(guest_ids_process,
               name=self.transfer_variable.intersect_guest_ids_process.name,
               tag=self.transfer_variable.generate_transferid(self.transfer_variable.intersect_guest_ids_process),
               role=consts.GUEST,
               idx=0)
        LOGGER.info("Remote guest_ids_process to Guest.")

        # recv intersect ids
        intersect_ids = None
        if self.get_intersect_ids_flag:
            encrypt_intersect_ids = get(name=self.transfer_variable.intersect_ids.name,
                                        tag=self.transfer_variable.generate_transferid(
                                            self.transfer_variable.intersect_ids),
                                        idx=0)

            intersect_ids_pair = encrypt_intersect_ids.join(host_ids_process_pair, lambda e, h: h)
            intersect_ids = intersect_ids_pair.map(lambda k, v: (v, "intersect_id"))
            LOGGER.info("Get intersect ids from Guest")

            if not self.only_output_key:
                intersect_ids = self._get_value_from_data(intersect_ids, data_instances)

        return intersect_ids


class RawIntersectionHost(RawIntersect):
    def __init__(self, intersect_params):
        super().__init__(intersect_params)
        self.join_role = intersect_params.join_role
        self.role = consts.HOST

    def run(self, data_instances):
        LOGGER.info("Start raw intersection")

        if self.join_role == consts.GUEST:
            intersect_ids = self.intersect_send_id(data_instances)
        elif self.join_role == consts.HOST:
            intersect_ids = self.intersect_join_id(data_instances)
        else:
            raise ValueError("Unknown intersect join role, please check the configure of host")

        return intersect_ids

class IntersectHost(ModelBase):
    def __init__(self):
        super().__init__()
        self.model_param = IntersectParam()
        self.intersect_num = -1
        self.intersect_rate = -1

    def fit(self, data):
        if self.model_param.intersect_method == "rsa":
            LOGGER.info("Using rsa intersection")
            intersection_obj = RsaIntersectionHost(self.model_param)
        elif self.model_param.intersect_method == "raw":
            LOGGER.info("Using raw intersection")
            intersection_obj = RawIntersectionHost(self.model_param)
        else:
            raise TypeError("intersect_method {} is not support yet".format(self.model_param.intersect_method))

        intersect_ids = intersection_obj.run(data)
        LOGGER.info("Save intersect results")

        if intersect_ids:
            self.intersect_num = intersect_ids.count()
            self.intersect_rate = self.intersect_num * 1.0 / data.count()

        return intersect_ids

    def save_data(self):
        self.callback_metric(metric_name="intersect",
                             metric_namespace='intersection',
                             metric_data=[Metric("intersect_count", self.intersect_num),
                                          Metric("intersect_rate", self.intersect_rate)])