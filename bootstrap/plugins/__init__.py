import logging
import os.path
import traceback
from abc import abstractmethod
from importlib import util
from typing import Any, List

from bootstrap.e import PluginNotFoundException


class BasePlugin:
    plugins: List[Any] = []

    logger = logging.getLogger(__name__)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.plugins.append(cls)

    @staticmethod
    def get_plugin(name: str):
        for plugin in BasePlugin.plugins:
            if plugin.name == name:
                return plugin
        raise PluginNotFoundException(f"plugin {name} not found")

    @abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplementedError


def load_module(path: str):
    name = os.path.split(path)[-1]
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


path = os.path.abspath(__file__)
dirpath = os.path.dirname(path)

for fname in os.listdir(dirpath):
    if (
        not fname.startswith(".")
        and not fname.startswith("__")
        and fname.endswith(".py")
    ):
        try:
            load_module(os.path.join(dirpath, fname))
        except Exception:
            traceback.print_exc()
