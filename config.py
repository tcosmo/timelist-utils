import os

class Config(object):
    TL_DB_PATH = os.environ.get('TL_DB_PATH') or "/home/cosmo/Documents/projects/timelist-db"
