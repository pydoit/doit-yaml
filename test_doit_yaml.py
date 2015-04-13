import yaml
from doit.task import Task
from doit.action import CmdAction

from doit_yaml import YAML_Loader



class TestTask(object):
    @staticmethod
    def convert(yaml_str):
        data = yaml.load(yaml_str)
        loader = YAML_Loader()
        return list(loader.entry2tasks(data))

    def test_simple_cmd(self):
        got = self.convert("""
task:
  name: simple
  cmd: echo hi
""")
        assert 1 == len(got)
        task = got[0]
        assert isinstance(task, Task)
        assert task.name == 'simple'
        assert 1 == len(task.actions)
        assert isinstance(task.actions[0], CmdAction)
        assert task.actions[0]._action == 'echo hi'
