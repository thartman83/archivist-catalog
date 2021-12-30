###############################################################################
## record.py for catalog models module                                       ##
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
## The record model for the archivist catalog system
##
## }}}

### Record ## {{{
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import base64
from .dbbase import db, DBBase
from .tag import Tag
from .page import Page

class Record(DBBase):
    name = db.Column(db.String(100), nullable=False)
    extension = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    textlocation = db.Column(db.String(250), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    pagecount = db.Column(db.Integer, nullable=False)
    hashValue = db.Column(db.String(64), nullable=False)
    notes = db.Column(db.Text(length=1000))

    pages = db.relationship('Page')
    
    tags = db.relationship('Tag', secondary='tags', lazy='subquery',
                           backref=db.backref('records', lazy=True))

    def serialize(self):
        with open(self.location,'rb') as f:
            data = base64.b64encode(f.read())
            
        return {
            "id": self.id,
            "name": self.name,
            "extension": self.extension,
            "location": self.location,
            "data": data.decode('ascii'),
            "textlocation": self.textlocation,
            "size": self.size,
            "pagecount": self.pagecount,
            "hash": self.hashValue,
            "datecreate": self.datecreated.strftime('%Y-%m-%d %H:%M:%S'),
            "datemodified": self.datemodified.strftime('%Y-%m-%d %H:%M:%S'),
            "notes": self.notes,
            "pages": list(map(lambda p: p.serialize(), self.pages)),
            "tags": list(map(lambda t: t.serialize(), self.tags))
        }

## }}}
