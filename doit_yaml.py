"""load doit tasks from a YAML file"""

import yaml

from doit.task import dict_to_task, Task
from doit.cmd_base import TaskLoader

from doitpy.pyflakes import Pyflakes



def listify(val):
    """if not a list convert value to a one-element list"""
    return val if isinstance(val, list) else [val]


def conv_task(data):
    """convert a yaml-dict to Task"""
    if isinstance(data, str):
        name = data
        actions = [data]
    else:
        assert isinstance(data, dict)
        name = data['name']
        actions = listify(data['cmd'])
    yield Task(name, actions=actions)


def conv_pyflakes(data):
    """convert a yaml entry into a Pyflakes task"""
    if isinstance(data, str):
        pattern = '*' in data
        module = data
    else:
        assert isinstance(data, dict)
        pattern = False
        module = data['file']


    flakes = Pyflakes()
    list_taskd = flakes.tasks(module) if pattern else [flakes(module)]
    for taskd in list_taskd:
        taskd['name'] = 'pyflakes:{}'.format(taskd['name'])
        yield dict_to_task(taskd)



class YAML_Loader(TaskLoader):

    # convert a yaml-dict to Task
    CONV = {
        'task': conv_task,
        'pyflakes': conv_pyflakes,
    }

    def yaml2dict(self):
        """convert YAML file into dict"""
        with open('dodo.yaml') as fp:
            return yaml.safe_load(fp)

    def entry2tasks(self, entry):
        """convert a dict from YAML into tasks using appropriate converter"""
        assert len(entry) == 1
        conv_name, val = entry.items()[0]
        conv = self.CONV.get(conv_name, None)
        assert conv is not None, '{} has no converter'.format(conv_name)
        return (conv(item) for item in listify(val))


    def load_tasks(self, cmd, opt_values, pos_args):
        """implement TaskLoader API"""
        data = self.yaml2dict()
        task_list = []
        for entry in data:
            for task_gen in self.entry2tasks(entry):
                for task in task_gen:
                    task_list.append(task)
        config = {'verbosity': 2}
        return task_list, config


