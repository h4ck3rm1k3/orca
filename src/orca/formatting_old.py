# Orca
#
# Copyright 2004-2009 Sun Microsystems Inc.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., Franklin Street, Fifth Floor,
# Boston MA  02110-1301 USA.

"""Manages the formatting settings for Orca."""

__id__ = "$Id:$"
__version__ = "$Revision:$"
__date__ = "$Date:$"
__copyright__ = "Copyright (c) 2004-2009 Sun Microsystems Inc."
__license__ = "LGPL"

import copy
import pyatspi
import orca.settings as settings
from orca.formatting_consts import PAUSE_STR
from orca.formatting_consts import TUTORIAL_STR 
from orca.formatting_consts import TUTORIAL 
from orca.formatting_consts import MNEMONIC
from orca.formatting_consts import BRAILLE_TEXT

ROLENAME = 'roleName'
LABELANDNAME = 'labelAndName'

class Formatting(dict):
    '''
    class that manages the formatting for different events
    '''
    def __init__(self, script):
        dict.__init__(self)
        self._script = script
        #self.update(copy.deepcopy(formatting))

    def update(self, newDict):
        for key, val in list(newDict.items()):
            if key in self:
                if isinstance(self[key], dict) and isinstance(val, dict):
                    self[key].update(val)
                elif isinstance(self[key], str) \
                        and isinstance(val, str):
                    self[key] = val
                else:
                    # exception or such like, we are trying to murge
                    # incompatible trees.
                    # throw an exception?
                    print("an error has occured, cant murge dicts.")
            else:
                self[key] = val

    def getPrefix(self, **args):
        """Get a formatting string to add on to the end of
        formatting strings obtained by getFormat.

        Arguments expected in args:
        - mode: output mode, such as 'speech', 'braille'.
        - formatType: the type of formatting, such as
          'focused', 'basicWhereAmI', etc.
        """
        prefix = self[args['mode']]['prefix'][args['formatType']]
        return prefix

    def getSuffix(self, **args):
        """Get a formatting string to add on to the end of
        formatting strings obtained by getFormat.

        Arguments expected in args:
        - mode: output mode, such as 'speech', 'braille'.
        - role: the role, such as pyatspi.ROLE_TEXT
        - formatType: the type of formatting, such as
          'focused', 'basicWhereAmI', etc.
        """
        suffix = self[args['mode']]['suffix'][args['formatType']]
        return suffix

    def getString(self, **args):
        """Gets a human consumable string for a specific value
        (e.g., an indicator for a checkbox state).

        Arguments expected in args:
        - mode: output mode, such as 'speech', 'braille'.
        - stringType: the type of the string to get (see the dictionary above).
        """
        return self['strings'][args['mode']][args['stringType']]

    def getFormat(self, **args):
        """Get a formatting string for the given mode and formatType for a
        role (e.g., a where am I string for a text object).

        Arguments expected in args:
        - mode: output mode, such as 'speech', 'braille'.
        - role: the role, such as pyatspi.ROLE_TEXT
        - formatType: the type of formatting, such as
          'focused', 'basicWhereAmI', etc.
        """
        try:
            # First try to find the exact match.
            #
            format_str = self[args['mode']][args['role']][args['formatType']]
        except Exception as exp:
            print(exp)
            try:
                # Failing that, fallback to the 'unfocused' formatType
                # for the mode and role, if it exists.
                #
                format_str = self[args['mode']][args['role']]['unfocused']
            except Exception as exp:
                try:
                    # Failing that, fallback to the default for the
                    # formatType
                    #
                    format_str = self[args['mode']][
                        'default'][args['formatType']]
                except Exception as exp:
                    # Failing that, just used the default 'unfocused' format
                    #
                    format_str = self[args['mode']]['default']['unfocused']
        return format_str
