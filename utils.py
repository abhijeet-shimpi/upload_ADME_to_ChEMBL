'''
Reads config.ini to change the connection parameters into dictionary
'''
from configparser import ConfigParser

DEFAULT_CONFIG = 'config.ini'

def config(item: str = None) -> dict:
    parser = ConfigParser()

    # reading config.ini inside parser
    parser.read(DEFAULT_CONFIG)
    config = dict()

    # iterating over each sections of config.ini data
    for section in parser.sections():

        # converting sections elements in dict format and storing in config dict
        section_config = dict(parser.items(section))
        config[section] = section_config
    if item:
        return config.get(item, None)
    else:
        return config
