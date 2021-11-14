###############################################################################
## run.py for catalog                                                        ##
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
## Catalog is the record keeping container for the archivist system
##
## }}}
import os
from app.appfactory import create_app
from config import config

### run ## {{{
if __name__ == "__main__":
    config_type = os.environ.get('CONFIG')
    dbengine = os.environ.get('DBENGINE')
    log = open('log.txt', 'w')

    print("Building app", file=log)
    if dbengine == 'mysql':
        print("Using mysql", file=log)
        app = create_app(config.MySqlConfig)
    else:
        app = create_app(config.DevConfig())
        
    app.run(port=os.environ.get('PORT'), host='0.0.0.0')
        
## }}}
