###############################################################################
## test_record.py for archivist catalog record routes                        ##
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
## Unit tests and fixtures for testing record routes
##
## }}}

### test_record ## {{{
import pytest, json, base64
from datetime import datetime
from app.models import Record, db
from app.common import storage
from app import create_app
from config import TestConfig
from pathlib import Path
from time import sleep
from shutil import rmtree

checksum = '2ee20486d3b51eed3f850139af55c7ea'

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

@pytest.fixture(scope='module')
def record_data():

    with open('tests/data/SamplePDF.pdf', 'rb') as pdf:
        pdfbase64 = base64.b64encode(pdf.read())
        
    record_data = {
        'name': 'ARecord',
        'extension': 'pdf',
        'pagecount': 2,
        'data': pdfbase64.decode('ascii'),
        'notes': 'This is a new record',
        'tags': ['tag1', 'tag2']
        }

    yield record_data
    

def test_new_record(test_client, init_db, record_data):
    """
    GIVEN a catalog application
    WHEN the /record page is requested POST
    WHEN the POST data contains all required fields
    THEN check that the response is valid
    THEN check that the record is created in the database
    THEN check that the record data is saved to the application storage directory
    """

    resp = test_client.post('/record', json=record_data)
    assert resp.status_code == 200
    print(resp.json)
    assert resp.json['name'] == 'ARecord'
    assert resp.json['extension'] == 'pdf'
    assert resp.json['pagecount'] == 2
    assert resp.json['notes'] == 'This is a new record'
    assert resp.json['hash'] == checksum

    recordDir = storage.StorageLocations.RECORD
    p = storage.findCreateCurSubDir(recordDir).joinpath(resp.json['hash'])
    assert resp.json['location'] == str(p)

    assert Path(resp.json['location']).exists()

def test_new_record_no_data(test_client, init_db):
    """
    GIVEN a catalog application
    WHEN the /record page is request POST
    WHEN the POST data is missing
    THEN check that the response is invalid 400
    THEN check that the error message is correct
    """

    resp = test_client.post('/record')
    assert resp.status_code == 400
    assert 'No data in record request' in resp.json['msg']

def test_new_record_missing_all(test_client, init_db):
    """
    GIVEN a catalog application
    WHEN the /record page is request POST
    WHEN the POST data is missing the name parameter
    THEN check that the response is invalid 400
    THEN check that the error message is correct
    """

    resp = test_client.post('/record', json={})
    assert resp.status_code == 400
    assert "Missing required argument 'name'" in resp.json['msg']
    assert "Missing required argument 'data'" in resp.json['msg']
    assert "Missing required argument 'extension'" in resp.json['msg']

def test_get_record_by_name(test_client, init_db):
    """
    GIVEN a catalog application
    GIVEN a record of name 'ARecord' exists
    WHEN the /record/ARecord page is requested GET
    THEN check that the response is valid
    THEN check that the metadata is correct for ARecord
    """
    
    recordname = 'ARecord'
    resp = test_client.get('/record/{}'.format(recordname))
    assert resp.status_code == 200
    assert resp.json['name'] == 'ARecord'
    assert resp.json['extension'] == 'pdf'
    assert resp.json['pagecount'] == 2

    recordDir = storage.StorageLocations.RECORD
    p = storage.findCreateCurSubDir(recordDir).joinpath(resp.json['hash'])
    assert resp.json['location'] == str(p)
    assert resp.json['notes'] == 'This is a new record'
    assert resp.json['hash'] == checksum
    assert resp.json['datecreate'] is not None
    assert resp.json['datemodified'] is not None

def test_get_record_by_name_invalid(test_client, init_db):
    """
    GIVEN a catalog application
    GIVEN a record of name BRecord does not exist
    WHEN the /record/BRecord page is requested GET
    THEN check that the response is invalid 404
    THEN check that the error message is correct
    """

    recordname = 'BRecord'
    resp = test_client.get('/record/{}'.format(recordname))
    assert resp.status_code == 404
    assert resp.json['status'] == 'Invalid record'
    assert resp.json['msg'] == "Record name '{}' does not exist".format(recordname)

def test_get_record_by_id(test_client, init_db):
    """
    GIVEN a catalog application
    GIVEN a record of id 1 exists
    WHEN the /record/1 page is requested GET
    THEN check that the response is valid
    THEN check that the metadata is correct for ARecord
    """
    
    recordid = 1
    resp = test_client.get('/record/{}'.format(recordid))
    assert resp.status_code == 200
    assert resp.json['name'] == 'ARecord'
    assert resp.json['extension'] == 'pdf'
    assert resp.json['pagecount'] == 2

    recordDir = storage.StorageLocations.RECORD
    p = storage.findCreateCurSubDir(recordDir).joinpath(resp.json['hash'])
    assert resp.json['location'] == str(p)
    assert resp.json['notes'] == 'This is a new record'
    assert resp.json['hash'] == checksum
    assert resp.json['datecreate'] is not None
    assert resp.json['datemodified'] is not None

def test_get_record_by_id_invalid(test_client, init_db):
    """
    GIVEN a catalog application
    GIVEN a record of id 100 does not exist
    WHEN the /record/100 page is requested GET
    THEN check that the response is invalid 404
    THEN check that the error message is correct
    """

    recordid = 100
    resp = test_client.get('/record/{}'.format(recordid))
    assert resp.status_code == 404
    assert resp.json['status'] == 'Invalid record id'
    assert resp.json['msg'] == "Record id '{}' does not exist".format(recordid)

def test_update_record(test_client, init_db):
    """
    GIVEN a catalog application
    GIVEN a record of id 1 that exists
    WHEN the /record/1 page is requested PUT
    WHEN the PUT data contains a new name BRecord
    THEN check that the response is valid
    THEN check that the response contains the new name
    THEN check that the modified data is greater than before the request    
    """

    recordid = 1
    record = test_client.get('/record/{}'.format(recordid))
    print(record.json)
    orig_mod = datetime.strptime(record.json['datemodified'], '%Y-%m-%d %H:%M:%S')
    data = { "name": "BRecord" }

    # wait 1 second to make sure that the date modified is updated with the correct time
    sleep(1)
    resp = test_client.put('/record/{}'.format(recordid), json=data)
    assert resp.status_code == 200
    assert resp.json['name'] == 'BRecord'
    new_mod = datetime.strptime(resp.json['datemodified'], '%Y-%m-%d %H:%M:%S')
    assert new_mod > orig_mod

def test_update_record_invalid(test_client, init_db):
    """
    GIVEN a catalog application
    GIVEN a record of id 100 does not exists
    WHEN the /record/100 page is requested PUT
    WHEN the PUT data contains a new name BRecord
    THEN check that the response is invalid 404
    """

    recordid = 100
    data = { "name": "BRecord" }
    
    resp = test_client.put('/record/{}'.format(recordid), json=data)
    assert resp.status_code == 404
    assert resp.json['status'] == 'Invalid record id'
    assert resp.json['msg'] == "Record id '{}' does not exist".format(recordid)

def test_update_record_no_data(test_client, init_db):
    """
    GIVEN a catalog application
    GIVEN a record of id 1 that exists
    WHEN the /record/1 page is requested PUT
    WHEN the PUT data contains no data
    THEN check that the response is invalid 400
    THEN check that the response contains an appropriate error message
    """

    recordid = 1
    resp = test_client.put('/record/{}'.format(recordid))
    assert resp.status_code == 400
    assert resp.json['status'] == 'error'
    assert resp.json['msg'] == "No data was provided to update record"

def test_delete_record(test_client, init_db):
    """
    GIVEN a catalog application
    GIVEN a record of id 1 exists
    WHEN the /record/1 page is requested DELETE
    THEN check that the response is valid
    THEN check that the record no longer exists
    """

    recordid = 1
    resp = test_client.delete('/record/{}'.format(recordid))
    assert resp.status_code == 200
    assert resp.json['status'] == 'success'
    assert resp.json['msg'] == "Record '{}' was deleted".format(recordid)

def test_delete_record(test_client, init_db):
    """
    GIVEN a catalog application
    GIVEN a record of id 100 does not exist
    WHEN the record /record/100 page is requested DELETE
    THEN check that the response is invalid
    THEN check that the response message is appropriate
    """

    recordid = 100
    resp = test_client.delete('/record/{}'.format(recordid))
    assert resp.status_code == 404
    assert resp.json['status'] == 'Invalid record id'
    assert resp.json['msg'] == "Record '{}' does not exist".format(recordid)

def test_get_record_tags(test_client, init_db):
    """
    GIVEN a catalog application
    GIVEN a record of id 1 exists
    GIVEN record 1 has tags 'tag1' and 'tag2'
    WHEN the /record/1/tags is requested GET
    THEN check that the response is valid
    THEN check that the response has the tags 'tag1' and 'tag2'
    """

    recordid = 1
    resp = test_client.get('/record/{}/tags'.format(recordid))
    assert resp.status_code == 200
    assert len(resp.json['tags']) == 2
    assert 'tag1' in list(map(lambda t: t['name'], resp.json['tags']))
    assert 'tag2' in list(map(lambda t: t['name'], resp.json['tags']))

def test_add_record_tag(test_client, init_db):
    """
    GIVEN a catalog application
    GIVEN a record of id 1 exist
    GIVEN record 1 does not have tag3
    WHEN the /record/1/tags is request POST
    WHEN post data is [ 'tag3' ]
    THEN check that the response is valid
    THEN check that the record has the tag 'tag3'
    """

    test_client.post('/tag', json={ 'name': 'tag3' })
    recordid = 1

    data = { 'tags': ['tag3'] }
    resp = test_client.post('/record/{}/tags'.format(recordid), json=data)
    assert resp.status_code == 200

    tags = test_client.get('/record/{}/tags'.format(recordid))
    assert 'tag3' in list(map(lambda t: t['name'], tags.json['tags']))

def test_update_record_tags(test_client, init_db):
    """
    GIVEN a catalog application
    GIVEN a record of id 1 exist
    GIVEN record 1 has tags 'tag1', 'tag2', 'tag3'
    GIVEN tags 'tag4' and 'tag5' exists
    WHEN the /record/1/tags is requested PUT
    WHEN put data is [ 'tag4', 'tag5' ]
    THEN check that the response is valid
    THEN check that the record no longer has tags 'tag1', 'tag2'. 'tag3'
    THEN check that the record has tags 'tag4' and 'tag5'
    """

    newtags = [ 'tag4', 'tag5' ]
    oldtags = [ 'tag1', 'tag2', 'tag3' ]
    map(lambda t: test_client.post('/tag', json={ 'name': t }), newtags)

    recordid = 1
    
    data = { 'tags': newtags }
    resp = test_client.put('/record/{}/tags'.format(recordid), json=data)
    assert resp.status_code == 200

    record = test_client.get('/record/{}/tags'.format(recordid))
    assert record.status_code == 200
    assert len(record.json['tags']) == len(newtags)
    appliedtags = list(map(lambda t: t['name'], record.json['tags']))

    for t in oldtags:
        assert t not in appliedtags

    for t in newtags:
        assert t in appliedtags

def test_create_record_with_pages(test_client, init_db):
    """
    GIVEN a catalog application
    WHEN /record is requested POST
    WHEN POST data is a new record with page data
    THEN check that the response is valid
    THEN check that the record is created
    THEN check that the page records are created
    THEN check that the page records are valid in the db
    """

    

                              
## }}}
