###############################################################################
## initialize.py for Archivist Catalog Routes                                   ##
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

### initialize ## {{{

from ..models.dbbase import db
from ..common import storage
from flask import Blueprint, jsonify, request

init_bp = Blueprint('init', __name__, url_prefix='/init')

@init_bp.route('', methods=['POST','GET'])
def initialize():
    if request.method == 'POST':
        db.create_all()
        storage.initializeStorageDirs()

    return jsonify({ "success": "true" })

## }}}
