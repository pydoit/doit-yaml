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

    def test_dict(self):
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


    def test_str(self):
        got = self.convert("""task: echo hi""")
        assert 1 == len(got)
        task = got[0]
        assert task.name == 'echo hi'
        assert isinstance(task.actions[0], CmdAction)
        assert task.actions[0]._action == 'echo hi'


    def test_list_dict(self):
        got = self.convert("""
task:
  - name: one
    cmd: echo hi
  - name: two
    cmd: echo hello
""")
        assert 2 == len(got)
        assert got[0].name == 'one'
        assert got[0].actions[0]._action == 'echo hi'
        assert got[1].name == 'two'


    def test_list_str(self):
        got = self.convert("""
task:
  - echo hi
  - echo hello
""")
        assert 2 == len(got)
        assert got[0].name == 'echo hi'
        assert got[0].actions[0]._action == 'echo hi'
        assert got[1].name == 'echo hello'


    def test_multi_cmd(self):
        got = self.convert("""
task:
   name: one
   cmd:
    - echo foo
    - echo bar
""")
        assert 1 == len(got)
        task = got[0]
        assert task.name == 'one'
        assert 2 == len(task.actions)
        assert task.actions[0]._action == 'echo foo'
        assert task.actions[1]._action == 'echo bar'
