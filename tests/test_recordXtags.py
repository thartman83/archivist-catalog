###############################################################################
## test_recordXtags.py for archivist catalog test modules                    ##
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
## Unit tests for record and tag cross reference table
##
## }}}

### test_recordXtags ## {{{
import pytest, json
from datetime import datetime
from app.models import Record, Tag, db
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

@pytest.fixture(scope='module')
def init_db():
    db.create_all()

    yield db
    
    db.drop_all()

def test_new_record_with_tags(test_client, init_db):
    """
    GIVEN a catalog application
    WHEN the /record pag is requested POST
    WHEN the POST data contains all required fields
    WHEN the POST data contains the tag fields
    THEN check that the response is valid
    THEN check that the record is created in the database
    THEN check that the tag records were created
    THEN check that the tag records are associated with the record
    """

    data = {
        'name': 'ARecord',
        'extension': 'pdf',
        'pagecount': 2,
        'data': 'JVBERi0xLjcKCjEgMCBvYmogICUgZW50cnkgcG9pbnQKPDwKICAvVHlwZSAvQ2F0YWxvZwogIC9QYWdlcyAyIDAgUgo+PgplbmRvYmoKCjIgMCBvYmoKPDwKICAvVHlwZSAvUGFnZXMKICAvTWVkaWFCb3ggWyAwIDAgMjAwIDIwMCBdCiAgL0NvdW50IDEKICAvS2lkcyBbIDMgMCBSIF0KPj4KZW5kb2JqCgozIDAgb2JqCjw8CiAgL1R5cGUgL1BhZ2UKICAvUGFyZW50IDIgMCBSCiAgL1Jlc291cmNlcyA8PAogICAgL0ZvbnQgPDwKICAgICAgL0YxIDQgMCBSIAogICAgPj4KICA+PgogIC9Db250ZW50cyA1IDAgUgo+PgplbmRvYmoKCjQgMCBvYmoKPDwKICAvVHlwZSAvRm9udAogIC9TdWJ0eXBlIC9UeXBlMQogIC9CYXNlRm9udCAvVGltZXMtUm9tYW4KPj4KZW5kb2JqCgo1IDAgb2JqICAlIHBhZ2UgY29udGVudAo8PAogIC9MZW5ndGggNDQKPj4Kc3RyZWFtCkJUCjcwIDUwIFRECi9GMSAxMiBUZgooSGVsbG8sIHdvcmxkISkgVGoKRVQKZW5kc3RyZWFtCmVuZG9iagoKeHJlZgowIDYKMDAwMDAwMDAwMCA2NTUzNSBmIAowMDAwMDAwMDEwIDAwMDAwIG4gCjAwMDAwMDAwNzkgMDAwMDAgbiAKMDAwMDAwMDE3MyAwMDAwMCBuIAowMDAwMDAwMzAxIDAwMDAwIG4gCjAwMDAwMDAzODAgMDAwMDAgbiAKdHJhaWxlcgo8PAogIC9TaXplIDYKICAvUm9vdCAxIDAgUgo+PgpzdGFydHhyZWYKNDkyCiUlRU9G',
        'notes': 'This is a new record',
        'tags': ['tag1', 'tag2']
    }

    resp = test_client.post('/record', json=data)
    assert resp.status_code == 200
    assert resp.json['name'] == 'ARecord'
    assert resp.json['extension'] == 'pdf'
    assert resp.json['pagecount'] == 2
    assert resp.json['notes'] == 'This is a new record'
    assert resp.json['hash'] == 'bcd0fc693cc6e5f6bbcd753e1932f18c'

    recordDir = storage.StorageLocations.RECORD
    p = storage.findCreateCurSubDir(recordDir).joinpath(resp.json['hash'])
    assert resp.json['location'] == str(p)
    assert len(resp.json['tags']) == 2
    assert next(filter(lambda t: t['name'] == 'tag1',
                       resp.json['tags'])) is not None
    assert next(filter(lambda t: t['name'] == 'tag2',
                       resp.json['tags'])) is not None

    resp_tag1 = test_client.get('/tag/{}'.format('tag1'))
    assert resp_tag1.status_code == 200

    resp_tag2 = test_client.get('/tag/{}'.format('tag2'))
    assert resp_tag2.status_code == 200
    
def testGetRecordsByTagname(test_client, init_db):
    """
    GIVEN a catalog application
    GIVEN a record with a tag value of tag1
    WHEN the /tag/<tagname>/records page is requested GET
    THEN check that the response is valid
    THEN check that there is a record returned
    THEN check that the record has the right metadata
    """
    
    resp = test_client.get('/tag/tag1/records')
    assert resp.status_code == 200
    assert len(resp.json['records']) == 1
    assert resp.json['records'][0]['name'] == 'ARecord'

def testGetRecordsByTagnameInvalid(test_client,init_db):
    """
    GIVEN a catalog application
    GIVEN the tag 'tag5' does not exist
    WHEN the /tag/<tagname>/records page is requested GET
    THEN check that the response is invalid 404
    """

    tagname = 'tag5'
    resp = test_client.get('/tag/{}/records'.format(tagname))
    assert resp.status_code == 404
    assert resp.json['status'] == 'Invalid Tag'
    assert resp.json['msg'] == "Tag '{}' does not exist".format(tagname)

def testGetRecordsByTagnameNoRecords(test_client, init_db):
    """
    GIVEN a catalog application
    GIVEN a tag 'tag8' exists
    GIVEN that no records have 'tag'8'
    WHEN the /tag/tag8/records page is requested GET
    THEN check that the response is valid
    THEN check that the records json response is an empty list
    """

    tagname = 'tag8'
    r = test_client.post('/tag'.format(tagname),
                         json={ 'name': tagname })

    assert r.status_code == 200
    
    resp = test_client.get('/tag/{}/records'.format(tagname))
    assert resp.status_code == 200
    assert len(resp.json['records']) == 0
    
## }}}
