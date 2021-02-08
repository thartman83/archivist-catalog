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
from app.appfactory import create_app
from config.config import DevConfig

### run ## {{{
if __name__ == "__main__":
    app = create_app(DevConfig)
    app.run()
        
## }}}
