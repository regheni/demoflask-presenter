import os
import sys

from config import ConfigurationSet, config_from_yaml, config_from_env
from presenter import ROOT_PATH

PREFIX = "presenter"


def config():
    env = os.environ.get("env", "local")
    return ConfigurationSet(
        config_from_env(prefix=PREFIX),
        config_from_yaml(f"{ROOT_PATH}/src/presenter/configuration/{env}.yml", read_from_file=True),
    )
