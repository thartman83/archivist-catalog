###############################################################################
## scan.py for descry routes                                              ##
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

### scan ## {{{
from flask import Blueprint, request, jsonify
from PIL import Image
import sane

scan_bp = Blueprint('scan', __name__, url_prefix='/scan')

@scan_bp.route('', methods=['GET'])
def scanDocument():
    var = sane.init()
    devices = sane.get_devices()
    dev = sane.open(devices[0][0])
    dev.start()
    im = dev.snap()
    im.save('test.png')

    return jsonify(done='true', data=im, status=200)
    
## }}}
