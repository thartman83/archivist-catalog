###############################################################################
## mrmime.py for archivist catalog common modules                           ##
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
## Mime type functions 
##
## }}}

### mrmime ## {{{
import PyPDF4
from pathlib import Path
from PIL import Image
from pdf2image import convert_from_path
import io, pytesseract

class MimeBase(object):

    def __init__(self, mimetype):
        self.mimetype = mimetype

class PDFMime(MimeBase):

    def textify(self, filePath):
        pdf = open(str(filePath), 'rb')

        reader = PyPDF4.PdfFileReader(pdf)
        text = ""

        # Extract any text in the document
        for page in reader.pages:
            text += page.extractText()

        # Check to see if there are images that need to be OCR'd
        for page in reader.pages:
            if '/XObject' in page['/Resources']:
                xobjs = page['/Resources']['/XObject'].getObject()
                for obj in xobjs:
                    if xobjs[obj]['/Subtype'] == '/Image':
                        img = Image.open(io.BytesIO(xobjs[obj].getData()))
                        text = text + pytesseract.image_to_string(img)
         
        return text

    def paginate(self, filePath):
        imgs = convert_from_path(filePath)

        return imgs

def docMime(MimeBase):

    def textify(self):
        pass

    def paginate(self):
        pass

def imageMime(MimeBase):

    def textify(self):
        pass

    def paginate(self):
        pass

MrMime = {
    "application/pdf": PDFMime("application/pdf")
}


## }}}
