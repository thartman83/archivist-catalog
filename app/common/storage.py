###############################################################################
## storage.py for storage functions for the common module                    ##
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
## Storage functions for the archivist catalog
##
## }}}

### storage ## {{{

from flask import current_app
from pathlib import Path
from config import StorageLocations

## Initialize the storage area
def initializeStorageDirs():
    cfg = current_app.config

    # get the configuration specified storage root
    p = Path(cfg['STORAGE_LOCATION'])

    # Create the configuration based sub directories
    for location in StorageLocations:
        p.joinpath(cfg['SUBDIRS'][location]).mkdir()

## 
def storeObject(storageType, data, name):
    cfg = current_app.config

    storagePath = Path('{}/{}'.format(cfg['STORAGE_LOCATION'],
                                      cfg[storageType]))
    subdir = findSubDirStorageAvailable(storagePath, cfg)
    
##    num_files = len([f for f in os.listdir(path)if os.path.isfile(os.path.join(path, f))])

## return the path within a storage path of the next available location
## to store data
def findCreateSubDir(storagePath, cfg):
    pass
    

## }}}
