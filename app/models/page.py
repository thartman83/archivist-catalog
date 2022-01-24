###############################################################################
## page.py for archivist catalog models module                            ##
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
## Page model for the archivist catalog
##
## }}}

### page ## {{{

from .dbbase import DBBase, db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
import io
import base64

class Page(DBBase):
    order = db.Column(db.Integer, nullable = False)
    mimetype = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    size = db.Column(db.Integer, nullable = False)
    hashValue = db.Column(db.String(64), nullable = False)
    record_id = db.Column(db.Integer, db.ForeignKey('record.id'))

    def serialize(self):
        
        with Image.open(self.location,'r') as img:
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            data = base64.b64encode(buf.getvalue())
        
        return {
            'id': self.id,
            'order': self.order,
            'mimetype': self.mimetype,
            'location': self.location,
            'size': self.size,
            'hash': self.hashValue,
            'record_id': self.record_id,
            'data': data.decode('ascii')
        }

## }}}
