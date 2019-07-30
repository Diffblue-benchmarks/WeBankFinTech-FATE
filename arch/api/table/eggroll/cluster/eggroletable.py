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

# noinspection PyProtectedMember
from arch.api.cluster.eggroll import _DTable
from arch.api.table.table import Table


class EggRollTable(Table):
    """
    wrapper of _Dtable of :class:`arch.api.cluster.eggroll._DTable`
    """

    def __init__(self, d_table: _DTable):
        self._dtable = d_table
        self.schema = d_table.schema
        # noinspection PyProtectedMember
        self._partitions = d_table._partitions

    def get_dtable(self):
        return self._dtable

    def save_as(self, name, namespace, partition=None, use_serialize=True):
        return EggRollTable(self._dtable.save_as(name, namespace, partition, use_serialize))

    def put(self, k, v, use_serialize=True):
        return self._dtable.put(k, v, use_serialize)

    def put_all(self, kv_list: Iterable, use_serialize=True, chunk_size=100000):
        return self._dtable.put_all(kv_list, use_serialize, chunk_size)

    def get(self, k, use_serialize=True):
        return self._dtable.get(k, use_serialize)

    def collect(self, min_chunk_size=0, use_serialize=True):
        return self._dtable.collect(min_chunk_size, use_serialize)

    def delete(self, k, use_serialize=True):
        return self._dtable.delete(k, use_serialize)

    def destroy(self):
        return self._dtable.destroy()

    def count(self):
        return self._dtable.count()

    def put_if_absent(self, k, v, use_serialize=True):
        return self._dtable.put_if_absent(k, v, use_serialize)

    # noinspection PyPep8Naming
    def take(self, n=1, keysOnly=False, use_serialize=True):
        return self._dtable.take(n, keysOnly, use_serialize)

    # noinspection PyPep8Naming
    def first(self, keysOnly=False, use_serialize=True):
        return self._dtable.first(keysOnly, use_serialize)

    # noinspection PyProtectedMember
    def partitions(self):
        return self._dtable._partitions

    """
    computing apis
    """

    def map(self, func):
        return EggRollTable(self._dtable.map(func))

    def mapValues(self, func):
        return EggRollTable(self._dtable.mapValues(func))

    def mapPartitions(self, func):
        return EggRollTable(self._dtable.mapPartitions(func))

    def reduce(self, func):
        return self._dtable.reduce(func)

    def join(self, other: 'EggRollTable', func):
        return EggRollTable(self._dtable.join(other._dtable, func))

    def glom(self):
        return EggRollTable(self._dtable.glom())

    def sample(self, fraction, seed=None):
        return EggRollTable(self._dtable.sample(fraction, seed))

    def subtractByKey(self, other):
        return EggRollTable(self._dtable.subtractByKey(other))

    def filter(self, func):
        return EggRollTable(self._dtable.filter(func))

    def union(self, other: 'EggRollTable', func=lambda v1, v2: v1):
        return EggRollTable(self._dtable.union(other._dtable, func))

    def flatMap(self, func):
        return EggRollTable(self._dtable.flatMap(func))
