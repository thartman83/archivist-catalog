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
import pytest, json, base64
from app.common import storage
from app import create_app
from config import TestConfig
from pathlib import Path
from shutil import rmtree


@pytest.fixture(scope='module')
def test_client():
    app = create_app(TestConfig)

    client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    test_storage = Path(TestConfig.STORAGE_LOCATION)
    test_storage.mkdir()

    try:
        storage.initializeStorageDirs()
    except Exception as e:        
        print(e)
        rmtree(str(test_storage))
        ctx.pop()
        raise    

    yield client

    rmtree(str(test_storage))
    ctx.pop()    

def testStorageFoldersExist(test_client):
    for loc in storage.StorageLocations:
        p = Path(TestConfig.STORAGE_LOCATION).joinpath(
            TestConfig.SUBDIRS[loc])

        assert p.exists()

def test_FindCreateCurSubDir_first(test_client):
    """
    GIVEN a archivist catalog application
    GIVEN a storage location initialized
    GIVEN there are no subdirs in the records folder
    WHEN findCreateSubDir is called
    WHEN parameters is RECORD
    THEN 
    """

    p = storage.findCreateCurSubDir(storage.StorageLocations.RECORD)    
    assert str(p.parts[-1]) == '1'.zfill(TestConfig.SUBDIR_LENGTH)

def test_FindCreateCurSubDir_available(test_client):
    """
    GIVEN a archivist catalog application
    GIVEN a storage location initialized
    GIVEN the current subdir is not full
    WHEN findCreateCurSubDir is called
    WHEN parameters is RECORD
    THEN
    """

    p = storage.findCreateCurSubDir(storage.StorageLocations.RECORD)
    assert str(p.parts[-1]) == '1'.zfill(TestConfig.SUBDIR_LENGTH)

def test_FindCreateCurSubDir_full(test_client):
    """
    GIVEN a archivist catalog application
    GIVEN a storage location initialized
    GIVEN the current subdir is full
    WHEN findCreateCurSubDir is called
    WHEN parameters is RECORD
    """

    p = storage.findCreateCurSubDir(storage.StorageLocations.RECORD)

    # add the max number of files in the current path dir
    for i in range(TestConfig.MAX_SUBDIR_LIMIT):
        p.joinpath(str(i)).touch()

    p_next = storage.findCreateCurSubDir(storage.StorageLocations.RECORD)
    assert str(p) != str(p_next)
    assert int(str(p_next.parts[-1])) == int(str(p.parts[-1])) + 1
    assert p.exists()

def test_FindCreateCurSubDir_availableAgain(test_client):
    """
    GIVEN a archivist catalog application
    GIVEN a storage location initialized
    GIVEN the current subdir is not full
    WHEN findCreateCurSubDir is called
    WHEN parameters is RECORD
    THEN
    """

    p = storage.findCreateCurSubDir(storage.StorageLocations.RECORD)
    assert str(p.parts[-1]) == '2'.zfill(TestConfig.SUBDIR_LENGTH)

def testStoreObject(test_client):
    """
    GIVEN an archivist catalog application
    GIVEN a storage location is initialized
    WHEN storeObject is called
    WHEN parameters is RECORD, data, and a name
    THEN check that the record is created and exists as a file
    """
    data = base64.b64decode('JVBERi0xLjcKCjEgMCBvYmogICUgZW50cnkgcG9pbnQKPDwKICAvVHlwZSAvQ2F0YWxvZwogIC9QYWdlcyAyIDAgUgo+PgplbmRvYmoKCjIgMCBvYmoKPDwKICAvVHlwZSAvUGFnZXMKICAvTWVkaWFCb3ggWyAwIDAgMjAwIDIwMCBdCiAgL0NvdW50IDEKICAvS2lkcyBbIDMgMCBSIF0KPj4KZW5kb2JqCgozIDAgb2JqCjw8CiAgL1R5cGUgL1BhZ2UKICAvUGFyZW50IDIgMCBSCiAgL1Jlc291cmNlcyA8PAogICAgL0ZvbnQgPDwKICAgICAgL0YxIDQgMCBSIAogICAgPj4KICA+PgogIC9Db250ZW50cyA1IDAgUgo+PgplbmRvYmoKCjQgMCBvYmoKPDwKICAvVHlwZSAvRm9udAogIC9TdWJ0eXBlIC9UeXBlMQogIC9CYXNlRm9udCAvVGltZXMtUm9tYW4KPj4KZW5kb2JqCgo1IDAgb2JqICAlIHBhZ2UgY29udGVudAo8PAogIC9MZW5ndGggNDQKPj4Kc3RyZWFtCkJUCjcwIDUwIFRECi9GMSAxMiBUZgooSGVsbG8sIHdvcmxkISkgVGoKRVQKZW5kc3RyZWFtCmVuZG9iagoKeHJlZgowIDYKMDAwMDAwMDAwMCA2NTUzNSBmIAowMDAwMDAwMDEwIDAwMDAwIG4gCjAwMDAwMDAwNzkgMDAwMDAgbiAKMDAwMDAwMDE3MyAwMDAwMCBuIAowMDAwMDAwMzAxIDAwMDAwIG4gCjAwMDAwMDAzODAgMDAwMDAgbiAKdHJhaWxlcgo8PAogIC9TaXplIDYKICAvUm9vdCAxIDAgUgo+PgpzdGFydHhyZWYKNDkyCiUlRU9G')
    p = storage.storeObject(storage.StorageLocations.RECORD, data, 'aname')
    assert p.exists()
    
## }}}
