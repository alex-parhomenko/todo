import os
from packages.logger.logger import Logger
import configparser
from config import Config

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = os.path.join(ROOT_DIR, "sources")


def getFullFileName(fdir, fname):
    """Returns a full file name"""
    return os.path.join(fdir, fname)


def initConfig(section_name=None):
    fname = os.path.join(ROOT_DIR, "config.ini")
    config = configparser.ConfigParser()
    config.read(fname)
    return config if section_name is None else config[section_name]


def initLogger(name):
    config = initConfig()
    # fmt: off
    return Logger(
        name,
        source_dir=SOURCE_DIR,
        config=config[Config.SEC_LOGGER]
    )
    # fmt: on
