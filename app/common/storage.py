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

    dir = findCreateCurSubDir(storageType)
    new_obj = dir.joinpath(name)
    print(dir.exists())
    new_obj.write_bytes(data)

    return new_obj    

## return the path within a storage path of the next available location
## to store data
def findCreateCurSubDir(storagePath):
    cfg = current_app.config
    
    rootPath = Path(cfg['STORAGE_LOCATION']).joinpath(cfg['SUBDIRS'][storagePath])

    cur_int = len(list(rootPath.glob('*')))

    ## Check to see if any directories exist
    if cur_int == 0:
        cur_int = 1
        new_path = rootPath.joinpath(str(cur_int).zfill(cfg['SUBDIR_LENGTH']))
        new_path.mkdir()

        return new_path

    cur_path = rootPath.joinpath(str(cur_int).zfill(cfg['SUBDIR_LENGTH']))
    print(len(list(cur_path.glob('*'))))

    if len(list(cur_path.glob('*'))) >= cfg['MAX_SUBDIR_LIMIT']:
        next_int = cur_int + 1
        next_path = rootPath.joinpath(str(next_int).zfill(cfg['SUBDIR_LENGTH']))
        next_path.mkdir()
        return next_path
    else:
        return cur_path
        

## }}}
