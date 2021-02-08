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
## 
##
## }}}

### Record ## {{{
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db
from .dbbase import DBBase

class Record(DBBase):
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    pagecount = db.Column(db.Integer, nullable=False)
    hash = db.Column(db.String(64), nullable=False)
    notes = db.Column(db.Text(length=1000))

    def serialize(self):
        return { "id": self.id,
                 "name": self.name,
                 "location": self.location,
                 "size": self.size,
                 "pagecount": self.pagecount,
                 "hash": self.hash,
                 "datecreate": self.datecreated,
                 "datemodified": self.datemodified,
                 "notes": self.notes }

## }}}
