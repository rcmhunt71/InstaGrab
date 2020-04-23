import os
import typing

import yaml


class InstaCfg:
    def __init__(self, cfg_file):
        self.file = cfg_file
        self.config = self.read_cfg_file()

    def read_cfg_file(self) -> dict:
        """
        If the specified YAML file exists, read and return the contents.

        :return: dictionary of configuration parameters or empty dictionary
        """
        cfg = {}
        if os.path.exists(self.file):
            cfg = yaml.safe_load(open(self.file, "r"))
        return cfg

    def get_element(self, path: typing.List[str], default: typing.Any) -> typing.Any:
        """
        Traverses the config to quickly get the necessary requested value
        :param path:
        :param default:
        :return:
        """
        location = self.config

        print(f"PATH: {path}")

        for elem in path[0:-1]:
            location = location.get(elem, {})
        return location.get(path[-1], default)
