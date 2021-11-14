###############################################################################
## appfactory.py for catalog                                                 ##
## Copyright (c) 2020 Tom Hartman (thomas.lees.hartman@gmail.com)            ##
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

### appfactory ## {{{
from flask import Flask
from config.config import DevConfig
from flask_sqlalchemy import SQLAlchemy
from .routes.record import record_bp
from .routes.initialize import init_bp
from .routes.tag import tag_bp
from .routes.status import status_bp
from .models.dbbase import db

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)

    app.register_blueprint(record_bp)
    app.register_blueprint(tag_bp)
    app.register_blueprint(init_bp)
    app.register_blueprint(status_bp)

    return app

# @app.cli.command()
# def createdb():
#     db.create_all()
    
## }}}
