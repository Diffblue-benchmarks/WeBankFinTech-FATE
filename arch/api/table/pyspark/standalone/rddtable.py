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

import uuid
from typing import Iterable

from pyspark import SparkContext

from arch.api import RuntimeInstance
from arch.api.table.eggroll.standalone.eggroletable import EggRollTable
from arch.api.table.pyspark import materialize, STORAGE_LEVEL
from arch.api.table.table import Table


class RDDTable(Table):

    def __init__(self, rdd=None, eggroll_table: EggRollTable = None, partitions=1, name=None, namespace=None):

        if rdd is None and eggroll_table is None:
            raise AssertionError("params rdd and storage are both None")
        self._rdd = rdd
        self._partitions = partitions
        self.eggroll_table = eggroll_table
        self.schema = {}
        self.name = name
        self.namespace = namespace

    # self._rdd should not be pickled since all transformer/action should be invoked in driver.
    def __getstate__(self):
        state = dict(self.__dict__)
        if "_rdd" in state:
            del state["_rdd"]
        return state

    @staticmethod
    def get_job_id():
        return RuntimeInstance.TABLE_MANAGER.get_job_id()

    @property
    def rdd(self):
        if hasattr(self, "_rdd") and self._rdd is not None:
            return self._rdd

        if self.eggroll_table is None:
            raise AssertionError("try create rdd from None storage")

        if self.eggroll_table.count() <= 0:
            raise AssertionError("can't create rdd from empty storage")

        storage_iterator = self.eggroll_table.collect(use_serialize=True)
        num_partition = self.eggroll_table.partitions()
        self._rdd = SparkContext.getOrCreate() \
            .parallelize(storage_iterator, num_partition) \
            .persist(STORAGE_LEVEL)
        return self._rdd

    @property
    def partitions(self):
        return self._partitions

    def map(self, func):
        rtn_rdd = self.rdd.map(
            lambda x: func(x[0], x[1]),
            preservesPartitioning=True)
        rtn_rdd = materialize(rtn_rdd)
        return RDDTable(rdd=rtn_rdd, partitions=rtn_rdd.getNumPartitions())

    def mapValues(self, func):
        rtn_rdd = self.rdd.mapValues(func)
        rtn_rdd = materialize(rtn_rdd)
        return RDDTable(rdd=rtn_rdd, partitions=rtn_rdd.getNumPartitions())

    def mapPartitions(self, func):
        rtn_rdd = self.rdd.mapPartitions(
            lambda x: [[str(uuid.uuid1()), func(x)]],
            preservesPartitioning=True)
        rtn_rdd = materialize(rtn_rdd)
        #         rtn_rdd = rtn_rdd.zipWithUniqueId()
        #         rtn_rdd = rtn_rdd.map(lambda x: (x[1], x[0])).persist(StorageLevel.MEMORY_AND_DISK)
        return RDDTable(rdd=rtn_rdd, partitions=rtn_rdd.getNumPartitions())

    def reduce(self, func):
        return self.rdd.values().reduce(func)

    def join(self, other, func=None):
        _partitions = max(self.partitions, other.partitions)
        rtn_rdd = self.rdd.join(other.rdd, numPartitions=_partitions)
        if func is not None:
            rtn_rdd = rtn_rdd.mapValues(lambda x: func(x[0], x[1]))
        rtn_rdd = materialize(rtn_rdd)
        return RDDTable(rdd=rtn_rdd, partitions=rtn_rdd.getNumPartitions())

    def glom(self):
        rtn_rdd = self.rdd.glom()
        rtn_rdd = materialize(rtn_rdd)
        return RDDTable(rdd=rtn_rdd, partitions=rtn_rdd.getNumPartitions())

    def sample(self, fraction, seed=None):
        rtn_rdd = self.rdd.sample(withReplacement=False, fraction=fraction, seed=seed)
        rtn_rdd = materialize(rtn_rdd)
        return RDDTable(rdd=rtn_rdd, partitions=rtn_rdd.getNumPartitions())

    def subtractByKey(self, other):
        raise NotImplementedError("subtractByKey is not implemented")

    def filter(self, func):
        rtn_rdd = self.rdd.filter(func)
        rtn_rdd = materialize(rtn_rdd)
        return RDDTable(rdd=rtn_rdd, partitions=rtn_rdd.getNumPartitions())

    def union(self, other, func=lambda v1, v2: v1):
        raise NotImplementedError("union is not implemented")

    def flatMap(self, func):
        raise NotImplementedError("flatMap is not implemented")

    def collect(self, min_chunk_size=0, use_serialize=True):
        if self.eggroll_table:
            return self.eggroll_table.collect(min_chunk_size, use_serialize)
        else:
            return iter(self.rdd.collect())

    """
    storage api
    """

    def put(self, k, v, use_serialize=True):
        return self.eggroll_table.put(k, v, use_serialize)

    def put_all(self, kv_list: Iterable, use_serialize=True, chunk_size=100000):
        return self.eggroll_table.put_all(kv_list, use_serialize, chunk_size)

    def get(self, k, use_serialize=True):
        return self.eggroll_table.get(k, use_serialize)

    def delete(self, k, use_serialize=True):
        return self.eggroll_table.delete(k, use_serialize)

    def destroy(self):
        return self.eggroll_table.destroy()

    def put_if_absent(self, k, v, use_serialize=True):
        return self.eggroll_table.put_if_absent(k, v, use_serialize)

    # noinspection PyPep8Naming
    def take(self, n=1, keysOnly=False, use_serialize=True):
        return self.eggroll_table.take(n, keysOnly, use_serialize)

    # noinspection PyPep8Naming
    def first(self, keysOnly=False, use_serialize=True):
        return self.eggroll_table.first(keysOnly, use_serialize)

    def count(self):
        if self.eggroll_table:
            return self.eggroll_table.count()
        else:
            return self.rdd.count()

    # noinspection PyProtectedMember
    def save_as(self, name, namespace, partition=None, use_serialize=True, persistent=True):
        if partition is None:
            partition = self._partitions
        partition = min(partition, 50)
        dup = RuntimeInstance.TABLE_MANAGER. \
            table(name=name, namespace=namespace, partition=partition, persistent=persistent)

        from arch.api.table.pyspark.standalone.rdd_func import _save_as_func
        res = self.rdd.mapPartitions(_save_as_func(dup))
        res.foreachPartition(lambda x: None)
        return dup

    def for_remote(self):
        if self.eggroll_table is None:
            return self.save_as(str(uuid.uuid1()), self.get_job_id(), partition=self.partitions, persistent=False)
        else:
            # noinspection PyProtectedMember
            return self.eggroll_table._dtable
