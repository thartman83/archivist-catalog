###############################################################################
## scanner.py for descry                                                     ##
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
## Provides a route that returns information on the scanner
##
## }}}

### scanner ## {{{
from flask import Blueprint, request, jsonify
import sane

scanner_bp = Blueprint('scanner', __name__, url_prefix='/scanner')

@scanner_bp.route('', methods=['GET'])
def getScanners():
    ver = sane.init()
    devs = sane.get_devices()
    return jsonify(devs)

## }}}
