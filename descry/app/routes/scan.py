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
import pytesseract

scan_bp = Blueprint('scan', __name__, url_prefix='/scan')

@scan_bp.route('', methods=['GET'])
def scanDocument():
    var = sane.init()
    devices = sane.get_devices()
    dev = sane.open(devices[0][0])
    scan_iter = dev.multi_scan()

    res = []
    page_num = 1

    while True:
        try:
            i = scan_iter.next()
            txt = OCRImage(i)
            dict = { "page": page_num, data: i.getdata() }
            res.insert(dict)
            page_num = page_num + 1
            
        except StopIteration:
            break
    
    return jsonify({ "status" : "done", "pages" : res, "page_count": page_num-1 })

def OCRImage(img):
    # orient the image properly
    img = orientImage(img)
    return pytesseract.image_to_string(img)
    
def orientImage(img):
    osdInfo = pytesseract.image_to_osd(img)
    parts = tuple(map(lambda x: x.split(': '), pytesseract.split('\n')))

    rotation = int(next(filter(lambda x: x[0] == 'Rotate', parts))[1])
    return img.rotate(rotation)
    
## }}}
