import subprocess
from typing import List, Union

from bootstrap import plugins
from bootstrap.e import BootstrapException


class CommandNotAllowedException(BootstrapException):
    pass


class BootstrapRuntimeError(BootstrapException):
    pass


class ScriptPlugin(plugins.BasePlugin):

    name: str = "script"

    command: str
    args: List[str]

    command_allowed: List[str] = ["shell"]

    def __init__(self):
        self.logger.info("plugin gitlab loaded")

    def run(
        self,
        command: str,
        args: Union[str, List[str]],
        workdir: str = None,
        *arg,
        **kwargs
    ):
        if command not in self.command_allowed:
            raise CommandNotAllowedException
        if isinstance(args, list):
            for script in args:
                yield getattr(self, command)(script, workdir)
        elif isinstance(args, str):
            yield getattr(self, command)(args, workdir)
        else:
            raise BootstrapRuntimeError

    def shell(self, command: str, workdir: str = None):
        return subprocess.check_output(command, shell=True, cwd=workdir)
