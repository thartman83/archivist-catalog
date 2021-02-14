###############################################################################
## record.py for catalog routes package                                     ##
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
from flask import Blueprint, request, jsonify
from ..models.record import Record
from ..models.dbbase import db

storagePath = ""
record_bp = Blueprint('record', __name__, url_prefix='/record')

@record_bp.route('', methods=['POST'])
def createRecord():
    json = request.get_json()
    hash, path = saveFileToStorage(json['data'])

    r = Record(name=json['name'],
               location=path,
               size=size(json['data']),
               extension=json['extension'],
               pagecount=json['pagecount'],
               hash=hash.hexdigest())

    db.session.add(r)
    db.session.commit()
    
    return jsonify(r.serialize())

@record_bp.route('/<id>', methods=['GET'])
def getRecord(id):
    r = Record.query.filter_by(id=id).first_or_404()

    return jsonify(r.serialize())

def saveFileToStorage(data):
    decodedData = base64.b64decode(data.encode('ascii'))

    hash = hashlib.md5(decodedData)
    path = hash.hexdigest()
    with open(path, 'wb+') as fh:
        fh.write(decodedData)

    return hash, path

def size(b64string):
    return (len(b64string) * 3) / 4 - b64string.count('=', -2)
## }}}
