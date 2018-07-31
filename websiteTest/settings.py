from configparser import ConfigParser
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PREFIX_CHECKS = 'check'

config = ConfigParser()
with open(os.path.join(BASE_DIR, 'conf', 'config.cfg'), 'r') as f:
    config.read_string(f.read())

