###############################################################################
## test_tags.py for archivist catalog unit tests                             ##
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
## Unit tests for tag routes and models
##
## }}}

### test_tags ## {{{
import pytest, json
from app.models import Tag
from app import create_app
from config import TestConfig
from app.models import db

@pytest.fixture(scope='module')
def test_client():
    app = create_app(TestConfig)

    client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    
    yield client
    ctx.pop()

@pytest.fixture(scope='module')
def init_db():
    db.create_all()

    # insert some data
    t1 = Tag(name="tag1")
    t2 = Tag(name="tag2")
    db.session.add(t1)
    db.session.add(t2)

    db.session.commit()

    yield db
    
    db.drop_all()

### Test the creation routes
def test_new_tag(test_client, init_db):
    """
    GIVEN a catalog application
    WHEN the /tag page is requested (POST)
    THEN check that the response is valid
    THEN check that a Tag is created in the database
    """
    data = { "name": "tag3" }
    resp = test_client.post('/tag',
                            json=data)    
    
    assert resp.status_code == 200
    assert resp.json['name'] == 'tag3'
    assert resp.json['id'] is not None

def test_new_existing_tag(test_client, init_db):
    """
    GIVEN a catalog application
    WHEN the /tag page is requested (POST)
    WHEN POST data is an existing tag name
    THEN check that the response is valid
    THEN check that the response has an existing error message
    """
    tagname = 'tag3'
    resp = test_client.post('/tag',
                            json={"name": tagname})
    assert resp.status_code == 400
    assert resp.json['status'] == "error"
    assert resp.json['msg'] == "Tag '{}' already exists".format(tagname)

def test_new_empty_tag(test_client, init_db):
    """
    GIVEN a catalog application
    WHEN the /tag page is requested (POST)
    WHEN the POST data is missing
    THEN check that the response is invalid (400)
    Then check that the error code that name is required parameter
    """

    resp = test_client.post('/tag')

    assert resp.status_code == 400
    assert resp.json['status'] == 'Invalid Request'
    assert resp.json['msg'] == "Required field 'name' not found"

def test_new_malformed_tag(test_client, init_db):
    """
    GIVEN a catalog application
    WHEN the /tag page is requested (POST)
    WHEN the POST data is malformed
    THEN check that the response is invalid (400)
    Then check that the error code that name is required parameter
    """

    resp = test_client.post('/tag', json={"foo": "bar"})

    assert resp.status_code == 400
    assert resp.json['status'] == 'Invalid Request'
    assert resp.json['msg'] == "Required field 'name' not found"
    

### Test the read routes
def test_get_tag(test_client, init_db):
    """
    GIVEN a catalog application
    GIVEN a Tag 'tag1' has been added
    WHEN the /tag/tag1 page is requested (GET)
    THEN check that the response is valid
    THEN check that the Tag data is valid
    """

    resp = test_client.get('/tag/tag1')

    assert resp.status_code == 200
    assert resp.json['name'] == 'tag1'
    assert resp.json['id'] is not None

def test_tag_does_not_exist(test_client, init_db):
    """
    GIVEN a catalog application
    GIVEN that dne does not exist as a tag
    WHEN the /tag/dne page is requested (GET)
    THEN check that the response is invalid 404
    THEN check that the response indicates the tag does not exist
    """

    tagname = 'dne'
    resp = test_client.get('/tag/{}'.format(tagname))

    assert resp.status_code == 404
    assert resp.json['status'] == 'error'    
    assert resp.json['msg'] == "Tag '{}' does not exist".format(tagname)

### Test the update routes
def test_update_tag(test_client, init_db):
    """
    GIVEN a catalog application
    GIVEN that tag Tag1 exists
    WHEN the /tag/tag1 page is requested (PUT)
    WHEN the PUT data contains {new_name: newtag}
    THEN check that the response is valid
    THEN check that the Tag tag1 is renamed to newtag
    """
    tagname = 'tag1'
    newtagname = 'newtag'
    tagid = test_client.get('/tag/{}'.format(tagname)).json['id']

    assert tagid is not None

    resp = test_client.put('/tag/{}'.format(tagname), json={"new_name": newtagname} )
    assert resp.status_code == 200
    assert resp.json['id'] == tagid
    assert resp.json['name'] == newtagname

def test_update_nonexistant_tag(test_client, init_db):
    """
    GIVEN a catalog application
    GIVEN that the tag dne does not exist
    WHEN the /tag/dne page is requested (PUT)
    WHEN the PUT data contains {new_name: newtag}
    THEN check that the response is invalid 404
    THEN check that the error messgae indicates the tag does not exist
    """

    tagname = 'dne'
    newtagname = 'newtag'
    resp = test_client.put('/tag/{}'.format(tagname), json={"new_name":newtagname})

    assert resp.status_code == 404
    assert resp.json["status"] == "error"
    assert resp.json["msg"] == "Tag {} does not exist".format(tagname)

def test_update_tag_missing_data(test_client, init_db):
    """
    GIVEN a catalog application
    GIVEN that the tag tag2 exists
    WHEN the /tag/tag2 page is requested (PUT)
    WHEN the PUT data is missing
    THEN check that the response is invalid 400
    THEN check that the error message indicates the required fields
    """

    tagname = 'tag2'
    resp = test_client.put('/tag/{}'.format(tagname))
    assert resp.status_code == 400
    assert resp.json['status'] == 'Invalid Request'
    assert resp.json['msg'] == "Update tag request missing required field 'new_name'"

def test_update_tag_malformed_data(test_client, init_db):
    """
    GIVEN a catalog application
    GIVEN that the tag tag2 exists
    WHEN the /tag/tag2 page is requested (PUT)
    WHEN the PUT data is malformed
    THEN check that the response is invalid 400
    THEN check that the error message indicates the required fields
    """

    tagname = 'tag2'
    resp = test_client.put('/tag/{}'.format(tagname), json={'foo':'bar'})
    assert resp.status_code == 400
    assert resp.json['status'] == 'Invalid Request'
    assert resp.json['msg'] == "Update tag request missing required field 'new_name'"

def test_delete_tag(test_client, init_db):
    """
    GIVEN a catalog application
    GIVEN that the tag tag2 exists
    WHEN the /tag/tag2 page is requested (DELETE)
    THEN check that the response is valid
    THEN check that the status is success
    THEN check that /tag/tag2 returns 404
    """

    tagname = 'tag2'
    resp = test_client.delete('/tag/{}'.format(tagname))
    assert resp.status_code == 200
    assert resp.json['status'] == 'success'
    resp2 = test_client.get('/tag/{}'.format(tagname))
    assert resp2.status_code == 404

def test_delete_missing_tag(test_client, init_db):
    """
    GIVEN a catalog application
    GIVEN that the tag tag2 does not exist
    WHEN the /tag/tag2 page is requested (DELETE)
    THEN check that the response is invalid 404
    THEN check that the message is tag does not exist
    """

    tagname = 'tag2'
    resp = test_client.delete('/tag/{}'.format(tagname))
    assert resp.status_code == 404
    assert resp.json['msg'] == "Tag '{}' does not exist".format(tagname)
                            
    
## }}}
