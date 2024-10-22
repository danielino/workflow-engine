import logging
import pathlib

import yaml

from bootstrap.workflow import Workflow

logging.basicConfig(level=logging.DEBUG)


def main():
    conf = yaml.safe_load(pathlib.Path("./workflow.yaml").read_text())
    workflow = Workflow(conf)
    workflow.execute()


if __name__ == "__main__":
    main()
