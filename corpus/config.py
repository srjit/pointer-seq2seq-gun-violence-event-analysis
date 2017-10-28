import configparser 

__author__ = "Sreejith Sreekumar"
__email__ = "sreekumar.s@husky.neu.edu"
__version__ = "0.0.1"


config_file = "config.cfg"
config = None


def read():
    """
       Returns the external configurations for the program
    """

    global config
    if config is None:
        config = configparser.RawConfigParser()   
        config.read(config_file)

    return config
    
