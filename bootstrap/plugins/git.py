from typing import List

import git
import path as libpath

from bootstrap import plugins
from bootstrap.e import BootstrapException


class CommandNotAllowedException(BootstrapException):
    pass


class GitPlugin(plugins.BasePlugin):

    name: str = "git"

    command: str
    args: List[str]

    command_allowed: List[str] = ["clone_repo", "merge_repo", "commit", "create_repo"]

    def __init__(self):
        self.logger.info("plugin gitlab loaded")

    def run(self, command: str, args: dict, *arg, **kwargs):
        if command not in self.command_allowed:
            raise CommandNotAllowedException
        yield getattr(self, command)(**args)

    def clone_repo(
        self,
        url: str,
        path: str = None,
        overwrite: bool = False,
        username: str = None,
        password: str = None,
        ref: str = "main",
    ):
        """
        clone a git repository under specific directory
        :param url:
        :param path:
        :param overwrite:
        :param username:
        :param password:
        :param ref:
        :return:
        """
        print(f"clone repo from url {url}")
        if overwrite:
            self.logger.debug("delete existing directory")
            libpath.Path(path).rmtree()
        repo = git.Repo.clone_from(url, path, branch=ref)
        return True

    def merge_branch(self, source: str, destination: str, *args, **kwargs):
        raise NotImplementedError

    def commit(self, *args, **kwargs):
        raise NotImplementedError

    def create_repo(self, name: str, path: str, *args, **kwargs):
        print(f"creating repo under {path}/{name}")
