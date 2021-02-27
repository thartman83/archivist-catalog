###############################################################################
## config.py for catalog                                                     ##
## Copyright (c) 2020 Tom Hartman (thomas.lees.hartman@gmail.com)            ##
##                                                                           ##
## This program is free software; you can redistribute it and/or             ##
## modify it under the terms of the GNU General Public License               ##
## as published by the Free Software Foundation; either version 2            ##
## of the License, or the License, or (at your option) any later             ##
## version.                                                                  ##
##                                                                           ##
## This program is distributed in the hope that it will be useful,           ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of            ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             ##
## GNU General Public License for more details.                              ##
###############################################################################

### Commentary ## {{{
##
## 
##
## }}}

### config ## {{{
from enum import Enum

class StorageLocations(Enum):
    TEXT = 1
    PAGES = 2
    RECORD = 3

class Config(object):
    DEBUG = False
    TESTING = False

    # the length of subdir numerical length ie: length of 4 is 0001, 0002
    SUBDIR_LENGTH = 4
    # the limit of the number of files within a storage subfolder
    MAX_SUBDIR_LIMIT = 500

    SUBDIRS = {
        StorageLocations.TEXT: "text",
        StorageLocations.PAGES: "pages",
        StorageLocations.RECORD: "records"
    }

class DevConfig(Config):
    DEBUG = True
    TESTING = False
    ENVIRONMENT = "DEV"
    SQLALCHEMY_DATABASE_URI="sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS=False

    STORAGE_LOCATION = 'storage/'

class TestConfig(Config):
    DEBUG = True
    TESTING = True
    ENVIRONMENT = "TEST"
    SQLALCHEMY_DATABASE_URI="sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS=False

    STORAGE_LOCATION = 'storage/'

class ProdConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "mysql://archivist:archivist@127.0.0.1/archivist"
## }}}
