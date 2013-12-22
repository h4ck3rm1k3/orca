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
