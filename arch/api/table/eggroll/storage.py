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
from arch.api.table.table import Storage


class EggRollStorage(Storage):
    """
    Storage Implemented by EggRoll, used by RDDTable
    """
    def __init__(self, dtable: _DTable):
        self._dtable: _DTable = dtable

    # @staticmethod
    # def create(_type, namespace, name, partitions):
    #     return EggRollStorage(_DTable(_type=_type, namespace=namespace, name=name, partitions=partitions))

    def __str__(self):
        return self._dtable.__str__()

    def put(self, k, v, use_serialize=True) -> bool:
        return self._dtable.put(k, v, use_serialize=use_serialize)

    def put_all(self, kv_list: Iterable, use_serialize=True, chunk_size=100000):
        return self._dtable.put_all(kv_list=kv_list, use_serialize=use_serialize, chunk_size=chunk_size)

    def put_if_absent(self, k, v, use_serialize=True):
        return self._dtable.put_if_absent(k=k, v=v, use_serialize=use_serialize)

    def get(self, k, use_serialize=True):
        return self._dtable.get(k=k, use_serialize=use_serialize)

    def collect(self, min_chunk_size=0, use_serialize=True):
        return self._dtable.collect(min_chunk_size=min_chunk_size, use_serialize=use_serialize)

    # noinspection PyPep8Naming
    def first(self, keysOnly=False, use_serialize=True):
        return self._dtable.first(keysOnly=keysOnly, use_serialize=use_serialize)

    # noinspection PyPep8Naming
    def take(self, n=1, keysOnly=False, use_serialize=True):
        return self._dtable.take(n=n, keysOnly=keysOnly, use_serialize=use_serialize)

    def save_as(self, name, namespace, partition=None, use_serialize=True):
        dtable = self._dtable.save_as(name=name, namespace=namespace, partition=partition, use_serialize=use_serialize)
        return EggRollStorage(dtable)

    def count(self):
        return self._dtable.count()

    def delete(self, k, use_serialize=True):
        return self._dtable.delete(k, use_serialize=use_serialize)

    def destroy(self):
        return self._dtable.destroy()

    # noinspection PyProtectedMember
    def partitions(self) -> int:
        return self._dtable._partitions
