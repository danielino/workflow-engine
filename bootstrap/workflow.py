from typing import List

from bootstrap import plugins
from bootstrap.e import StepsNotFoundException

_plugins = plugins.BasePlugin.plugins


class Step:

    plugin: plugins.BasePlugin
    command: str
    args: dict

    def __init__(self, parent_job, *args, **kwargs):
        self.job = parent_job
        _plugin = kwargs.pop("plugin")
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.plugin = plugins.BasePlugin.get_plugin(_plugin)

    def execute(self, *args, **kwargs):
        print(self.__dict__)
        yield from self.plugin().run(**self.__dict__)


class Job:
    steps: List[Step] = []

    def __init__(self, parent_workflow, *args, **kwargs):
        self.workflow = parent_workflow
        self.name = kwargs["name"] or None
        kwargs.pop("name")

        assert "steps" in kwargs.keys(), StepsNotFoundException(self.workflow)

        for step in kwargs["steps"]:
            self.steps.append(Step(parent_job=self, **step))

        kwargs.pop("steps")

        for k, v in kwargs.items():
            setattr(self, k, v)


class Workflow:
    jobs: List[Job] = []

    def __init__(self, workflow: dict):
        for job in workflow["jobs"]:
            self.jobs.append(Job(parent_workflow=self, **job))

    def execute(self):
        for job in self.jobs:
            for step in job.steps:
                # iterate over yield
                for _exec in step.execute():
                    print(_exec)
