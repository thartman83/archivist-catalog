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
from flask import Blueprint, request, jsonify
from ..models import Record
from ...config import DevConfig

record_bp = Blueprint('record', __name__, url_prefix='/record')
config = DevConfig()

@recipe_bp.route('', methods=['POST'])
def createRecipe():
    data = request.json('data')
    saveFileToStorage(data)


def saveFileToStorage(data):
    decodedData = base64.decodebytes(data)
    hash = hashlib.md5(decodedData)
    path = config.storage + "/" + hash
    with open(path) as fh:
        fh.write(decodedData)

    return hash, 
## }}}
