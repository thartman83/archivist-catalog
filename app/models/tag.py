###############################################################################
## tag.py for catalog models module                                      ##
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
## Tag model for catalog
##
## }}}

### tag ## {{{
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from ..models.dbbase import db
from .dbbase import DBBase

class Tag(DBBase):
    name = db.Column(db.String(20), nullable=False)

    def serialize(self):
        return { "id": self.id,
                 "name": self.name
               }

## Xref table
# tags = db.Table('tags',
#                 db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),                          
#                 db.Column('record_id', db.Integer, db.ForeignKey('record.id')))
## }}}
