import sys
from configparser import ConfigParser

DEFAULT_CONFIG = 'config.ini'


def config(item: str = None) -> dict:
    parser = ConfigParser()
    parser.read(DEFAULT_CONFIG)
    config = dict()
    for section in parser.sections():
        section_config = dict(parser.items(section))
        config[section] = section_config
    if item:
        return config.get(item, None)
    else:
        return config
