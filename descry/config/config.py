###############################################################################
## config.py for descry                                                      ##
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

### config ## {{{
class Config(object):
    DEBUG = False
    TESTING = False

class ProdConfig(Config):
    portno = 8123
    host = '127.0.0.1'

class DevConfig(Config):
    portno = 8123
    host = '127.0.0.1'

class TestingConfig(Config):
    portno = 8123
    host = '127.0.0.1'

## }}}
