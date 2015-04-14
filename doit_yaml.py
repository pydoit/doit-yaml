"""load doit tasks from a YAML file"""

import yaml

from doit.task import dict_to_task, Task
from doit.cmd_base import TaskLoader


def listify(val):
    """if not a list convert value to a one-element list"""
    return val if isinstance(val, list) else [val]


def task_conv(data):
    """convert a yaml-dict to Task"""
    if isinstance(data, str):
        name = data
        actions = [data]
    else:
        assert isinstance(data, dict):
        name = data['name']
        actions = listify(data['cmd'])
    return Task(name, actions=actions)



class YAML_Loader(TaskLoader):

    # convert a yaml-dict to Task
    CONV = {'task': task_conv}

    def yaml2dict(self):
        """convert YAML file into dict"""
        with open('dodo.yaml') as fp:
            return yaml.safe_load(fp)

    def entry2tasks(self, entry):
        """convert a dict from YAML into tasks using appropriate converter"""
        assert len(entry) == 1
        cls_name, val = entry.items()[0]
        cls = self.CONV.get(cls_name, None)
        assert cls is not None, '{} has no converter'.format(cls_name)
        return (cls(item) for item in listify(val))


    def load_tasks(self, cmd, opt_values, pos_args):
        """implement TaskLoader API"""
        data = self.yaml2dict()
        task_list = []
        for entry in data:
            for task in self.entry2tasks(entry):
                task_list.append(task)
        config = {'verbosity': 2}
        return task_list, config


