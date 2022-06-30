import os
from packages.logger.logger import Logger
from sys import path
import configparser
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = os.path.join(ROOT_DIR, 'sources')


def getFullFileName(fdir, fname):
    '''Returns a full file name
    '''
    return os.path.join(fdir, fname)


def initConfig():
    fname = os.path.join(ROOT_DIR, 'config.ini')
    config = configparser.ConfigParser()
    config.read(fname)
    return config


def initLogger(name):
    config = initConfig()
    return Logger(name, source_dir=SOURCE_DIR, config=config['logger'])
