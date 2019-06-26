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
from typing import List
from fate_flow.manager import model_manager
from fate_flow.db.db_models import DB, Job, Task
from fate_flow.storage.fate_storage import FateStorage
from fate_flow.entity.metric import Metric, MetricMeta
from arch.api.utils.core import current_timestamp


class Tracking(object):
    METRIC_DATA_PARTITION = 48
    METRIC_LIST_PARTITION = 48

    def __init__(self, job_id: str, component_name: str = None, task_id: str = None, model_id: str = None):
        self.job_id = job_id
        self.component_name = component_name
        self.task_id = task_id
        self.table_namespace = '_'.join(['fate_flow', 'tracking', 'data', self.job_id, self.component_name])
        self.model_id = model_id
        self.model_version = self.job_id

    def log_metric_data(self, metric_namespace: str, metric_name: str, metrics: List[Metric]):
        kv = {}
        for metric in metrics:
            kv[metric.key] = metric.value
        FateStorage.save_data(kv.items(), namespace=self.table_namespace,
                              name=Tracking.metric_table_name(metric_namespace, metric_name),
                              partition=Tracking.METRIC_DATA_PARTITION, create_if_missing=True, error_if_exist=True)

    def read_metric_data(self, metric_namespace: str, metric_name: str):
        kv = FateStorage.read_data(namespace=self.table_namespace,
                                   name=Tracking.metric_table_name(metric_namespace, metric_name))
        metrics = []
        for k, v in kv:
            metrics.append(Metric(key=k, value=v))
        metrics.sort(key=lambda x: x.key)
        return metrics

    def set_metric_meta(self, metric_namespace: str, metric_name: str, metric_meta: MetricMeta):
        FateStorage.save_data_table_meta(metric_meta.to_dict(), namespace=self.table_namespace,
                                         name=Tracking.metric_table_name(metric_namespace, metric_name))

    def get_metric_meta(self, metric_namespace: str, metric_name: str):
        kv = FateStorage.get_data_table_meta(namespace=self.table_namespace,
                                             name=Tracking.metric_table_name(metric_namespace, metric_name))
        return MetricMeta(name=kv.get('name'), metric_type=kv.get('metric_type'), extra_metas=kv)

    def put_into_metric_list(self, metric_namespace: str, metric_name: str):
        kv = {'%s:%s' % (metric_namespace, metric_name): metric_name}
        FateStorage.save_data(kv, namespace=self.table_namespace, name=Tracking.metric_list_table_name(),
                              partition=Tracking.METRIC_LIST_PARTITION, create_if_missing=True, error_if_exist=True)

    def get_metric_list(self):
        kv = FateStorage.read_data(namespace=self.table_namespace, name=Tracking.metric_list_table_name())
        metrics = dict()
        for k, v in kv:
            metric_namespace = k.rstrip(':%s' % v)
            metrics[metric_namespace] = metrics.get(metric_namespace, [])
            metrics[metric_namespace].append(v)
        return metrics

    def save_output_data_table(self, data_table, data_name: str = 'component'):
        FateStorage.save_data({data_name: {'name': data_table._name, 'namespace': data_name._namespace}} if data_table else {},
                              name=Tracking.output_table_name('data'),
                              namespace=self.table_namespace,
                              partition=48)

    def get_output_data_table(self, data_name: str = 'component'):
        output_data_info_table = FateStorage.table(name=Tracking.output_table_name('data'),
                                                   namespace=self.table_namespace)
        data_table_info = output_data_info_table.get(data_name)
        if data_table_info:
            return FateStorage.table(name=data_table_info.get('name', ''),
                                     namespace=data_table_info.get('namespace', ''))
        else:
            return None

    def save_output_model(self, model_buffers: dict):
        """

        :param model_buffers:
        {"ProtobufferClassName": ProtobufferObject}
        :return:
        """
        model_manager.save_model(model_key=self.component_name if self.component_name else 'pipeline',
                                 model_buffers=model_buffers,
                                 model_version=self.model_version,
                                 model_id=self.model_id)

    def get_output_model(self):
        return model_manager.read_model(model_key=self.component_name if self.component_name else 'pipeline',
                                        model_version=self.model_version,
                                        model_id=self.model_id)

    @DB.connection_context()
    def save_job_info(self, role, party_id, job_info, create=False):
        jobs = Job.select().where(Job.f_job_id == self.job_id, Job.f_role == role, Job.f_party_id == party_id)
        is_insert = True
        if jobs:
            job = jobs[0]
            is_insert = False
        elif create:
            job = Job()
            job.f_create_time = current_timestamp()
        else:
            return None
        job.f_job_id = self.job_id
        job.f_role = role
        job.f_party_id = party_id
        if 'f_status' in job_info:
            if job.f_status in ['success', 'failed', 'partial', 'deleted']:
                # Termination status cannot be updated
                # TODO:
                pass
        for k, v in job_info.items():
            if k in ['f_job_id', 'f_role', 'f_party_id'] or v is None:
                continue
            setattr(job, k, v)
        if is_insert:
            job.save(force_insert=True)
        else:
            job.save()
        return job

    @DB.connection_context()
    def save_task(self, role, party_id, task_info, create=False):
        tasks = Task.select().where(Task.f_job_id == self.job_id,
                                    Task.f_component_name == self.component_name,
                                    Task.f_task_id == self.task_id,
                                    Task.f_role == role,
                                    Task.f_party_id == party_id)
        is_insert = True
        if tasks:
            task = tasks[0]
            is_insert = False
        elif create:
            task = Task()
            task.f_create_time = current_timestamp()
        else:
            return None
        task.f_job_id = self.job_id
        task.f_component_name = self.component_name
        task.f_task_id = self.task_id
        task.f_role = role
        task.f_party_id = party_id
        if 'f_status' in task_info:
            if task.f_status in ['success', 'failed', 'partial', 'deleted']:
                # Termination status cannot be updated
                # TODO:
                pass
        for k, v in task_info.items():
            if k in ['f_job_id', 'f_component_name', 'f_task_id', 'f_role', 'f_party_id'] or v is None:
                continue
            setattr(task, k, v)
        if is_insert:
            task.save(force_insert=True)
        else:
            task.save()
        return task

    @staticmethod
    def metric_table_name(metric_namespace: str, metric_name: str):
        return '_'.join(['metric', metric_namespace, metric_name])

    @staticmethod
    def metric_list_table_name():
        return '_'.join(['metric', 'list'])

    @staticmethod
    def output_table_name(output_type: str):
        return '_'.join(['output', output_type])


if __name__ == '__main__':
    FateStorage.init_storage()
    tracker = Tracking('123456', 'hetero_lr')
    metric_namespace = 'TRAIN'
    metric_name = 'LOSS0'
    tracker.log_metric_data(metric_namespace, metric_name, [Metric(1, 0.2), Metric(2, 0.3)])

    metrics = tracker.read_metric_data(metric_namespace, metric_name)
    for metric in metrics:
        print(metric.key, metric.value)

    tracker.set_metric_meta(metric_namespace, metric_name, MetricMeta(name=metric_name, metric_type='LOSS', extra_metas={'BEST': 0.2}))
    metric_meta = tracker.get_metric_meta(metric_namespace, metric_name)
    print(metric_meta.name, metric_meta.metric_type, metric_meta.metas)
