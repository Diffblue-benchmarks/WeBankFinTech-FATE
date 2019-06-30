#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from arch.api.utils import log_utils
from federatedml.param.base_param import BaseParam

LOGGER = log_utils.getLogger()


class OneHotEncoderParam(object):
    """

    Parameters
    ----------

    cols: list or int, default: -1
        Specify which columns need to calculated. -1 represent for all columns.

    """

    def __init__(self, cols=-1):
        self.cols = cols

    def check(self):
        descr = "One-hot encoder param's"
        self.check_defined_type(self.cols, descr, ['list', 'int'])
        return True
