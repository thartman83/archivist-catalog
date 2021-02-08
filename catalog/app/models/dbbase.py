###############################################################################
## dbbase.py for catalog models module                                       ##
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
## dbbase is the base object model for catalog models
##
## }}}

### dbbase ## {{{
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import datetime
from app import db

class DBBase(db.Model):
    __abstract__ = True
    __table_args__ = { "mysql_engine":"InnoDB" }
    id = db.Column(db.Integer, primary_key=True)
    datecreated = db.Column(db.DatTime, server_default=func.now())
    datemodified = db.Column(db.DatTime, server_default=func.now())

## }}}
