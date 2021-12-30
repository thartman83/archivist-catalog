###############################################################################
## status.py for catalog route module                                        ##
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
## Status page for the Archivist catalog microservice
##
## }}}

### status ## {{{
import os
from flask import Flask, Blueprint, request, jsonify
from ..models.dbbase import db

status_bp = Blueprint('status', __name__, url_prefix='/status')

@status_bp.route('',methods=['GET'])
def status():
    engine = db.get_engine()
    return jsonify({
        'up': True,
        'environment': {
            'dbhost': os.environ.get('MYSQL_HOST'),
            'database': os.environ.get('MYSQL_DATABASE'),
            'dbengine': os.environ.get('DBENGINE'),
            'dbuser': os.environ.get('MYSQL_USER'),
            'storage_location': os.environ.get('STORAGE_LOCATION')
        },
        'database': {
            'engine': {
                'dialect': engine.dialect.name,
                'table_names': engine.table_names()
                },
            'config': {
                'database': engine.url.database,
                'driver': engine.url.drivername,
                'host': engine.url.host,
                'port': engine.url.port,
                'username': engine.url.username
                },
            'initialized': (len(engine.table_names()) != 0)
            }        
        })

## }}}
