#coding=utf8

import os

from tornado.options import define

define('debug', default=True)
define("port", default=8888, help="run on the given port", type=int)

# remove '/config'
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))[:-6]

#print PROJECT_ROOT
IMAGE_ROOT = '/static/img/'

UPLOAD_DIR = PROJECT_ROOT + 'static'
PLATFORM = 'sina'


ADMIN_LIST = [1659901275, 1751091154]

MAX_PACKAGE_COUNT = 100
