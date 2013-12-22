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

from . import settings


from formatting_const import PAUSE_STR
from formatting_const import TUTORIAL_STR 
from formatting_const import TUTORIAL 
from formatting_const import MNEMONIC
from formatting_const import BRAILLE_TEXT



if settings.useExperimentalSpeechProsody:
    use_experimental_speech_prosody()

ROLENAME = 'roleName'
LABELANDNAME = 'labelAndName'

def use_experimental_speech_prosody(formatting):
    '''
    create the formatting for prosody
    '''
    formatting[ 'speech'][ pyatspi.ROLE_CANVAS][ 'focused'] = _add(
        LABELANDNAME,
        'imageDescription',
        'roleName',
        PAUSE_STR,
        'positionInList')

    formatting[ 'speech'][ pyatspi.ROLE_CANVAS][ 'unfocused'] = _add(
        LABELANDNAME,
        'imageDescription',
        'roleName',
        PAUSE_STR,
        'positionInList'
    )

    formatting['speech'][pyatspi.ROLE_CANVAS]['basicWhereAmI'] =  _add(
        'parentRoleName',
        PAUSE_STR,
        LABELANDNAME,
        PAUSE_STR,
        'selectedItemCount',
        PAUSE_STR)

    formatting['speech'][pyatspi.ROLE_CANVAS]['detailedWhereAmI'] = _add(
        'parentRoleName',
        PAUSE_STR,
        LABELANDNAME,
        PAUSE_STR,
        'selectedItemCount',
        PAUSE_STR,
        'selectedItems',
        PAUSE_STR)

    formatting['speech'][pyatspi.ROLE_CHECK_MENU_ITEM]['unfocused'] = _add (
        LABELANDNAME,
        'roleName',
        'checkedState',
        'required',
        'availability',
        MNEMONIC,
        'accelerator',
        PAUSE_STR,
        'positionInList')

    formatting['speech'][pyatspi.ROLE_CHECK_MENU_ITEM]['basicWhereAmI'] = _add(
        'ancestors',
        PAUSE_STR,
        LABELANDNAME,
        'roleName',
        'checkedState',
        PAUSE_STR,
        'accelerator',
        PAUSE_STR,
        'positionInList',
        MNEMONIC)

    formatting['speech'][pyatspi.ROLE_COMBO_BOX]['focused'] = _add(
        'name',
        PAUSE_STR,
        'positionInList',
        PAUSE_STR)

    formatting[ 'speech'][ pyatspi.ROLE_COMBO_BOX][ 'unfocused'] = _add(
        'label',
        'name',
        'roleName',
        PAUSE_STR,
        'positionInList',
        MNEMONIC,
        'accelerator'
    )

    formatting['speech'][pyatspi.ROLE_COMBO_BOX]['basicWhereAmI' ] = _add (
        'label',
        'roleName',
        PAUSE_STR,
        'name',
        'positionInList',
        MNEMONIC,
        'accelerator')

    formatting['speech'][pyatspi.ROLE_HEADING]['basicWhereAmI'] = _add(
        'label',
        'readOnly',
        'textRole',
        PAUSE_STR,
        'textContent',
        'anyTextSelection',
        MNEMONIC)

    formatting['speech'][pyatspi.ROLE_HEADING]['detailedWhereAmI'] = _add(
        'label',
        'readOnly',
        'textRole',
        PAUSE_STR,
        'textContentWithAttributes',
        'anyTextSelection',
        MNEMONIC,
        TUTORIAL)

    formatting[ 'speech'][ pyatspi.ROLE_ICON][ 'focused'] = _add(
        LABELANDNAME,
        'imageDescription',
        'roleName',
        PAUSE_STR,
        'positionInList')

    formatting[ 'speech'][ pyatspi.ROLE_ICON][ 'unfocused'] = _add(
        LABELANDNAME,
        'imageDescription',
        ROLENAME,
        PAUSE_STR,
        'positionInList')

    formatting['speech'][pyatspi.ROLE_ICON]['basicWhereAmI'] = _add(
        'parentRoleName',
        PAUSE_STR,
        'labelAndName',
        PAUSE_STR,
        'selectedItemCount',
        PAUSE_STR)

    formatting['speech'][pyatspi.ROLE_ICON]['detailedWhereAmI'] = _add(
        'parentRoleName',
        PAUSE_STR,
        'labelAndName',
        PAUSE_STR,
        'selectedItemCount',
        PAUSE_STR,
        'selectedItems',
        PAUSE_STR)

    formatting['speech'][pyatspi.ROLE_LAYERED_PANE]['basicWhereAmI'] = _add (
        LABELANDNAME,
        PAUSE_STR,
        'roleName',
        PAUSE_STR,
        'selectedItemCount',
        PAUSE_STR)

    formatting['speech'][pyatspi.ROLE_LAYERED_PANE]['detailedWhereAmI'] = _add(
        'labelAndName',
        PAUSE_STR,
        ROLENAME,
        PAUSE_STR,
        'selectedItemCount',
        PAUSE_STR,
        'selectedItems',
        PAUSE_STR)

    formatting['speech'][pyatspi.ROLE_LINK]['basicWhereAmI'] = _add(
        'linkInfo',
        PAUSE_STR,
        'siteDescription',
        PAUSE_STR,
        'fileSize',
        PAUSE_STR,
        MNEMONIC)

    formatting['speech'][pyatspi.ROLE_LIST]['unfocused'] = _add(
        'labelOrName',
        PAUSE_STR,
        'focusedItem',
        PAUSE_STR,
        'multiselectableState',
        'numberOfChildren',
        PAUSE_STR)

    formatting['speech'][pyatspi.ROLE_LIST_ITEM]['unfocused'] = _add(
        LABELANDNAME,
        'allTextSelection',
        PAUSE_STR,
        'expandableState',
        PAUSE_STR,
        'availability',
        'positionInList',
        PAUSE_STR,
        'childWidget'
    )

    formatting['speech'][pyatspi.ROLE_LIST_ITEM]['basicWhereAmI'] = _add(
        'label',
        ROLENAME,
        PAUSE_STR,
        'name',
        PAUSE_STR,
        'positionInList',
        PAUSE_STR,
        'expandableState',
        '(nodeLevel or nestingLevel)',
        PAUSE_STR)

    formatting['speech'][pyatspi.ROLE_MENU]['unfocused'] = _add(
        LABELANDNAME,
        'allTextSelection',
        'roleName',
        'availability',
        MNEMONIC,
        'accelerator',
        PAUSE_STR,
        'positionInList')

    formatting['speech'][pyatspi.ROLE_MENU]['basicWhereAmI'] =  _add(
        '(ancestors or parentRoleName)',
        PAUSE_STR,
        LABELANDNAME,
        ROLENAME,
        PAUSE_STR,
        'positionInList',
        MNEMONIC)

    formatting['speech'][pyatspi.ROLE_MENU_ITEM]['unfocused'] = _add(
        LABELANDNAME,
        'menuItemCheckedState',
        'expandableState',
        'availability',
        MNEMONIC,
        'accelerator',
        PAUSE_STR,
        'positionInList'
    )

    formatting['speech'][pyatspi.ROLE_MENU_ITEM]['basicWhereAmI'] = _add(
        'ancestors',
        PAUSE_STR,
        'labelAndName',
        PAUSE_STR,
        'accelerator',
        PAUSE_STR,
        'positionInList',
        MNEMONIC)

    formatting[ 'speech'][ pyatspi.ROLE_PAGE_TAB][ 'focused'] = _add (
        LABELANDNAME,
        'roleName',
        PAUSE_STR,
        'positionInList',
        MNEMONIC,
        'accelerator')

    formatting[ 'speech'][ pyatspi.ROLE_PAGE_TAB][ 'unfocused'] = _add (
        LABELANDNAME,
        'roleName',
        PAUSE_STR,
        'positionInList',
        MNEMONIC,
        'accelerator')

    formatting['speech'][pyatspi.ROLE_PAGE_TAB]['basicWhereAmI'] = _add(
        'parentRoleName',
        PAUSE_STR,
        LABELANDNAME,
        'roleName',
        PAUSE_STR,
        'positionInList',
        MNEMONIC,
        'accelerator')

    formatting['speech'][pyatspi.ROLE_RADIO_BUTTON]['unfocused'] = _add(
        LABELANDNAME,
        PAUSE_STR,
        'radioState',
        'roleName',
        'availability',
        'lineBreak',
        MNEMONIC,
        'accelerator',
        PAUSE_STR,
        'positionInList',
        PAUSE_STR)

    formatting['speech'][pyatspi.ROLE_RADIO_BUTTON]['basicWhereAmI'] = _add(
        'radioButtonGroup',
        PAUSE_STR,
        LABELANDNAME,
        'roleName',
        PAUSE_STR,
        'radioState',
        PAUSE_STR,
        'positionInGroup',
        MNEMONIC,
        'accelerator')

    formatting['speech'][pyatspi.ROLE_TABLE]['focused'] = _add(
        LABELANDNAME,
        PAUSE_STR,
        'table' )

    formatting['speech'][pyatspi.ROLE_TABLE]['unfocused'] = _add(
        LABELANDNAME,
        PAUSE_STR,
        'table')

    formatting['speech'][pyatspi.ROLE_TABLE]['basicWhereAmI'] = _add(
        LABELANDNAME,
        PAUSE_STR,
        'table')

    formatting['speech'][pyatspi.ROLE_TABLE_CELL]['focused'] = _add(
        _add (

            " ". join(
                '((',
                _add ('tableCell2ChildLabel',
                     'tableCell2ChildToggle'),
            ') or cellCheckedState)'
            ),
            PAUSE_STR,
            '(expandableState and (' +
            _add(
                'expandableState',
                PAUSE_STR,
                'numberOfChildren',
                PAUSE_STR)
            +
            '))'
        ))

    formatting['speech'][pyatspi.ROLE_TABLE_CELL]['unfocused'] = _add(
        'tableCellRow',
        PAUSE_STR)



    formatting['speech'][pyatspi.ROLE_TABLE_CELL]['basicWhereAmI'] = _add(
        'parentRoleName',
        PAUSE_STR,
        'columnHeader',
        PAUSE_STR,
        'rowHeader',
        PAUSE_STR,
        'roleName',
        PAUSE_STR,
        'cellCheckedState',
        PAUSE_STR,
        _grp(
            _or('realActiveDescendantDisplayedText' ,
                _add (
                    'imageDescription',
                    'image'
                )
            )
        ),
        PAUSE_STR,
        'columnAndRow',
        PAUSE_STR,
        'expandableState',
        PAUSE_STR,
        'nodeLevel',
        PAUSE_STR)

    formatting['speech'][pyatspi.ROLE_TABLE_CELL]['detailedWhereAmI'] = _add(
        'parentRoleName',
        PAUSE_STR,
        'columnHeader',
        PAUSE_STR,
        'rowHeader',
        PAUSE_STR,
        'roleName',
        PAUSE_STR,
        'cellCheckedState',
        PAUSE_STR,
        _grp(
            _or('realActiveDescendantDisplayedText' ,
                _add (
                    'imageDescription',
                    'image'
                )
            )
        ),

        PAUSE_STR,
        'columnAndRow',
        PAUSE_STR,
        'tableCellRow',
        PAUSE_STR,
        'expandableState',
        PAUSE_STR,
        'nodeLevel',
        PAUSE_STR)

    formatting['speech'][pyatspi.ROLE_TERMINAL]['basicWhereAmI'] = _add(
        'label',
        'readOnly',
        PAUSE_STR,
        'textRole',
        PAUSE_STR,
        'textContent',
        'anyTextSelection',
        MNEMONIC)

    formatting['speech'][pyatspi.ROLE_TERMINAL]['detailedWhereAmI'] = _add(
        'label',
        'readOnly',
        PAUSE_STR,
        'textRole',
        PAUSE_STR,
        'textContentWithAttributes',
        'anyTextSelection',
        MNEMONIC,
        TUTORIAL)

    formatting['speech'][pyatspi.ROLE_TEXT]['focused'] = _add(
        'labelOrName',
        'placeholderText',
        'readOnly',
        'textRole',
        PAUSE_STR,
        'textIndentation',
        'currentLineText',
        'allTextSelection')

    formatting['speech'][pyatspi.ROLE_TEXT]['unfocused'] = _add(
        'labelOrName',
        'placeholderText',
        'readOnly',
        'textRole',
        PAUSE_STR,
        'textIndentation',
        'currentLineText',
        'allTextSelection',
        MNEMONIC)

    formatting['speech'][pyatspi.ROLE_TEXT]['basicWhereAmI'] = _add(
        'label',
        'placeholderText',
        'readOnly',
        'textRole',
        PAUSE_STR,
        'textContent',
        'anyTextSelection',
        PAUSE_STR,
        MNEMONIC)

    formatting['speech'][pyatspi.ROLE_TEXT]['detailedWhereAmI'] = _add(
        'label',
        'placeholderText',
        'readOnly',
        'textRole',
        PAUSE_STR,
        'textContentWithAttributes',
        'anyTextSelection',
        PAUSE_STR,
        MNEMONIC,
        TUTORIAL)

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
