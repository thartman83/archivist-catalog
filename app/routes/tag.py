###############################################################################
## tag.py for catalog route module                                           ##
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
## Tag route
##
## }}}

### tag ## {{{
from flask import Blueprint, request, jsonify
from ..models import Tag, Record, db

# Create the tag route blueprint that will be used for all of the tag routes
tag_bp = Blueprint('tag',__name__, url_prefix='/tag')

# Putting the C in CRUD
@tag_bp.route('',methods=['POST'])
def createTag():
    json = request.get_json()

    ## validate the request
    if json is None or 'name' not in json:
        return jsonify({
            "status": "Invalid Request",
            "msg": "Required field 'name' not found"
            }), 400

    name = json['name']

    t = Tag.query.filter_by(name=name).first()

    # check for duplicate tags
    if not t is None:
        return jsonify({
            "status": "error",
            "msg": "Tag '{}' already exists".format(name)
            }), 400
    
    t = Tag(name=name)
    db.session.add(t)
    db.session.commit()

    return jsonify(t.serialize())

# Gimmie an R
@tag_bp.route('/<name>', methods=['GET'])
def getTag(name):
    t = Tag.query.filter_by(name=name).first()

    if t is None:
        return jsonify({
            "status": "error",
            "msg": "Tag '{}' does not exist".format(name)
            }), 404

    return jsonify(t.serialize())

# U stands for update
@tag_bp.route('/<name>', methods=['PUT'])
def renameTag(name):
    json = request.get_json()
    if json is None or 'new_name' not in json:
        return jsonify({
            'status': 'Invalid Request',
            'msg': "Update tag request missing required field 'new_name'"
            }), 400

    new_name = json['new_name']        

    t = Tag.query.filter_by(name=name).first()
    if t is None:
        return jsonify( {
            "status": "error",
            "msg": "Tag {} does not exist".format(name)
            }), 404

    t.name = new_name
    db.session.commit()

    return jsonify(t.serialize())

# Gimmie that D
@tag_bp.route('/<name>', methods=['DELETE'])
def deleteTag(name):
    t = Tag.query.filter_by(name=name).first()

    if t is None:
        return jsonify( {
            "status": "error",
            "msg": "Tag '{}' does not exist".format(name)
            }), 404

    db.session.delete(t)
    db.session.commit()

    return jsonify({
        "status": "success"
        })

# Get all of the records based on a tag
@tag_bp.route('/<name>/records', methods=['GET'])
def getRecordsByTagName(name):
    t = Tag.query.filter_by(name=name).first()

    if t is None:
        return jsonify(
            {
              'status': 'Invalid Tag',
              'msg': "Tag '{}' does not exist".format(name)
            }), 404

    records = Record.query.filter(Record.tags.any(name=t.name)).all()
    return jsonify({ "records": list(map(lambda r: r.serialize(), records)) })

## }}}
