###############################################################################
## test_mrmime.py for archivist catalog unit test module                     ##
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
## Unit tests for mrmime
##
## }}}

### test_mrmime ## {{{

from app.common.mrmime import MrMime
from PIL import Image, ImageChops
from fuzzy_match import match, algorithims
import string

def test_pdfTextify():
    """
    GIVEN a PDFMime object
    WHEN the textify method is invoke
    WHEN the parameter passed is a valid pdf file path
    THEN the textify function will return the text of the pdf
    """
    
    pdfMime = MrMime["application/pdf"]
    pdfFile = "tests/data/SamplePDF.pdf"
    textFile = "tests/data/SampleText.txt"
    
    textified = pdfMime.textify(pdfFile)
    expectedText = ""

    with open(textFile, 'r') as file:
        expectedText = file.read()

    remove = expectedText.maketrans('','',string.whitespace + string.punctuation)
    assert textified.translate(remove) == expectedText.translate(remove)

def test_pdfTextifyOCR():
    """
    GIVEN a PDFMime object
    WHEN the textify method is invoke
    WHEN the parameter passed is a valid pdf file path with image data
    THEN the textify function will return the text of the pdf
    """
    
    pdfMime = MrMime["application/pdf"]
    pdfFile = "tests/data/SampleScan.pdf"
    textFile = "tests/data/SampleText.txt"
    
    textified = pdfMime.textify(pdfFile)
    expectedText = ""

    with open(textFile, 'r') as file:
        expectedText = file.read()

    remove = expectedText.maketrans('','',string.whitespace + string.punctuation)
    val = algorithims.trigram(textified.translate(remove),
                             expectedText.translate(remove))
    assert val >= .9

def test_pdfPaginate():
    """
    GIVEN a PDFMime object
    WHEN the textify method is invoke
    WHEN the parameter passed is a valid pdf file path
    THEN the paginate function will return the pages of the pdf
         as PIL images
    """

    pdfMime = MrMime["application/pdf"]
    pdfFile = "tests/data/SamplePDF.pdf"
    imgFileBase = "tests/data/SampleImages-{}.tif"

    pages = pdfMime.paginate(pdfFile)
    assert len(pages) == 2

    idx = 1
    for p in pages:
        imgPath = imgFileBase.format(idx)
        diff = ImageChops.difference(p, Image.open(imgPath)) 
        assert diff.getbbox()
        idx = idx + 1

## }}}
