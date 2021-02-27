###############################################################################
## test_storage.py for the archivist catalog test suite                      ##
## Copyright (c) 2021 Tom Hartman (thomas.lees.hartman@gmail.com)            ##
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
## Test cases for storage common functions
##
## }}}

### test_storage ## {{{
import pytest, json
from app.common import storage
from app import create_app
from config import TestConfig
from pathlib import Path

@pytest.fixture(scope='module')
def test_client():
    app = create_app(TestConfig)

    client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    storage.initializeStorageDirs()

    yield client

    ctx.pop()

def testStorageFoldersExist(test_client):
    for loc in storage.StorageLocations:
        p = Path(TestConfig['STORAGE_LOCATION']).joinpath(
            TestConfig['SUBDIRS'][loca])

        assert p.exists()
    
## }}}
