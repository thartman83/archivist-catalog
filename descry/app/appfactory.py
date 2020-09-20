###############################################################################
## appfactory.py for descry                                                     ##
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
from .routes.scanner import scanner_bp
from .routes.scan import scan_bp

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    app.register_blueprint(scanner_bp)
    app.register_blueprint(scan_bp)

    return app
## }}}
