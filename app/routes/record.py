###############################################################################
## record.py for catalog routes package                                      ##
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
## 
##
## }}}

### record ## {{{
import base64, hashlib
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from ..models.record import Record, Tag
from ..models.dbbase import db
from ..common import storage
#from ..models import db, Record, Tag

storagePath = ""
record_bp = Blueprint('record', __name__, url_prefix='/record')

@record_bp.route('', methods=['POST'])
def createRecord():
    json = request.get_json()

    ## Validate the record data and metadata
    valid, res = validateRecordData(json)
    if not valid:
        return jsonify(res), 400

    # Save the record data to the storage system
    try: 
        hash, filesize, path = saveFileToStorage(json.pop('data',None))
    except Exception as e:
        return jsonify(
            { 'status': 'error',
               'msg': 'An error occured while saving the record: {}'.format(e)
            }, 500)

    # Add caluclated and storage values, then add to the record dictionary
    json['location'] = str(path)
    json['hash'] = hash.hexdigest()
    json['size'] = filesize

    # pop the tags off (if they exist) and then create the record
    tags = json.pop('tags',None)

    r = Record(**json)

    if tags is not None:
        for t in tags:
            r.tags.append(Tag.findCreateTag(t))

    db.session.add(r)
    db.session.commit()
    
    return jsonify(r.serialize())

@record_bp.route('/<int:id>', methods=['GET'])
def getRecordById(id):
    r = Record.query.filter_by(id=id).first()

    if r is None:
        return jsonify({ 'status': 'Invalid record id',
                         'msg': "Record id '{}' does not exist".format(id)
                        }), 404

    return jsonify(r.serialize())

@record_bp.route('/<name>', methods=['GET'])
def getRecordByName(name):
    r = Record.query.filter_by(name=name).first()

    if r is None:
        return jsonify({ 'status': 'Invalid record',
                         'msg': "Record name '{}' does not exist".format(name)
                         }), 404

    return jsonify(r.serialize())

@record_bp.route('/<int:id>', methods=['PUT'])
def updateRecord(id):
    r = Record.query.filter_by(id=id).first()    

    if r is None:
        return jsonify({'status': 'Invalid record id',
                        'msg': "Record id '{}' does not exist".format(id)}), 404

    json = request.get_json()
    if json is None:
        return jsonify({'status': 'error',
                        'msg': 'No data was provided to update record'}), 400
    
    if 'name' in json:
        r.name = json['name']

    if 'notes' in json:
        r.notes = json['notes']

    db.session.commit()
    return jsonify(r.serialize())

@record_bp.route('/<int:id>', methods=['DELETE'])
def deleteRecord(id):
    r = Record.query.filter_by(id=id).first()

    if r is None:
        return jsonify({'status': 'Invalid record id',
                        'msg': "Record '{}' does not exist".format(id)}), 404

    db.session.delete(r)
    db.session.commit()

    return jsonify({'status': 'success',
                    'msg': "Record '{}' was deleted".format(id)})

@record_bp.route('/<int:id>/tags', methods=['GET'])
def getRecordTags(id):
    r = Record.query.filter_by(id=id).first()

    if r is None:
        return jsonify({'status': 'Invalid record id',
                        'msg': "Record '{}' does not exist".format(id)}), 404

    return jsonify({ 'tags': list(map(lambda t: t.serialize(), r.tags)) })

@record_bp.route('/<int:id>/tags', methods=['POST'])
def addRecordTag(id):
    r = Record.query.filter_by(id=id).first()

    if r is None:
        return jsonify({'status': 'Invalid record id',
                        'msg': "Record '{}' does not exist".format(id)}), 404

    json = request.get_json()
    if json is None:
        return jsonify({'status': 'error',
                        'msg': 'No data was provided to update record tags'}), 400

    tags = json['tags']
    for t in tags:
        r.tags.append(Tag.findCreateTag(t))

    db.session.commit()

    return jsonify({ 'status': 'success'})

@record_bp.route('/<int:id>/tags', methods=['PUT'])
def updateRecordTags(id):
    r = Record.query.filter_by(id=id).first()

    if r is None:
        return jsonify({'status': 'Invalid record id',
                        'msg': "Record '{}' does not exist".format(id)}), 404

    json = request.get_json()
    if json is None:
        return jsonify({'status': 'error',
                        'msg': 'No data was provided to update record tags'}), 400

    r.tags.clear()

    tags = []
    for tagname in json['tags']:
        tags.append(Tag.findCreateTag(tagname))

    for t in tags:
        r.tags.append(t)

    db.session.commit()

    return jsonify({ 'status': 'success' })

###### Route helper functions
def saveFileToStorage(data):
    decodedData = base64.b64decode(data.encode('ascii'))
    cfg = current_app.config
    
    hash = hashlib.md5(decodedData)
    path = storage.storeObject(storage.StorageLocations.RECORD,
                               decodedData, hash.hexdigest())

    return hash, size(data), path

## Return the size in bytes of the base64 encoded file stream
def size(b64string):
    return (len(b64string) * 3) / 4 - b64string.count('=', -2)

### validate the record data recieved from 
def validateRecordData(recordData):
    valid = True
    res = dict()
    invalidData = dict({ 'status': 'Invalid request', 'msg': [] })

    # check if there is any data at all
    if recordData is None:
        valid = False
        invalidData['msg'].append('No data in record request')
        return valid, invalidData

    # Check for the required name field
    if 'name' not in recordData:
        valid = False
        invalidData['msg'].append("Missing required argument 'name'")

    # Check that the record data is present
    if 'data' not in recordData:
        valid = False
        invalidData['msg'].append("Missing required argument 'data'")

    # Check that the extension data is present
    if 'extension' not in recordData:
        valid = False
        invalidData['msg'].append("Missing required argument 'extension'")

    return valid, invalidData
                  
    
## }}}
