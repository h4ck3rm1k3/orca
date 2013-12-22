
def speech():
    return {
        'speech': {
        'prefix': {
            'focused': '[]',
            'unfocused': 'oldAncestors + newAncestors + newRowHeader + newColumnHeader + newRadioButtonGroup',
            'basicWhereAmI': 'toolbar',
            'detailedWhereAmI' : '[]'
            },
        'suffix': {
            'focused': '[]',
            'unfocused': 'newNodeLevel + unselectedCell + ' + TUTORIAL,
            'basicWhereAmI': TUTORIAL + ' + description',
            'detailedWhereAmI' : '[]'
            },
        'default': {
            'focused': '[]',
            'unfocused': 'labelAndName + allTextSelection + roleName + availability + ' + MNEMONIC + ' + accelerator + childWidget',
            'basicWhereAmI': 'labelAndName + roleName',
            'detailedWhereAmI' : '[]'
            },
        pyatspi.ROLE_ALERT: {
            'unfocused': 'labelAndName + unrelatedLabels'
            },
        pyatspi.ROLE_ANIMATION: {
            'unfocused': 'labelAndName'
            },
        pyatspi.ROLE_CANVAS: {
            'focused': 'labelAndName + imageDescription + roleName + positionInList',
            'unfocused': 'labelAndName + imageDescription + roleName + positionInList',
            'basicWhereAmI': 'parentRoleName + labelAndName + selectedItemCount',
            'detailedWhereAmI': 'parentRoleName + labelAndName + selectedItemCount + selectedItems'
            },
        pyatspi.ROLE_CHECK_BOX: {
            'focused': 'checkedState',
            'unfocused': 'labelAndName + roleName + checkedState + required + availability + ' + MNEMONIC + ' + accelerator',
            'basicWhereAmI': 'namedContainingPanel + labelAndName + roleName + checkedState + ' + MNEMONIC + ' + accelerator + required'
            },
        pyatspi.ROLE_CHECK_MENU_ITEM: {
            'focused': 'checkedState',
            'unfocused': 'labelAndName + roleName + checkedState + required + availability + ' + MNEMONIC + ' + accelerator + positionInList',
            'basicWhereAmI': 'ancestors + labelAndName + roleName + checkedState + accelerator + positionInList + ' + MNEMONIC
            },
        pyatspi.ROLE_COLOR_CHOOSER: {
            'focused': 'value',
            'unfocused': 'label + roleName + value + required + availability + ' + MNEMONIC,
            'basicWhereAmI': 'label + roleName + value + percentage + ' + MNEMONIC + ' + accelerator + required'
            },
        pyatspi.ROLE_COMBO_BOX: {
            'focused': 'name + positionInList',
            'unfocused': 'label + name + roleName + positionInList + ' + MNEMONIC + ' + accelerator',
            'basicWhereAmI': 'label + roleName + name + positionInList + ' + MNEMONIC + ' + accelerator'
            },
        pyatspi.ROLE_DIALOG: {
            'unfocused': 'labelAndName + unrelatedLabels'
            },
        pyatspi.ROLE_DOCUMENT_FRAME: {
            'basicWhereAmI': 'label + readOnly + textRole + textContent + anyTextSelection + ' + MNEMONIC,
            'detailedWhereAmI': 'label + readOnly + textRole + textContentWithAttributes + anyTextSelection + ' + MNEMONIC + ' + ' + TUTORIAL
            },
        pyatspi.ROLE_EMBEDDED: {
            'focused': 'embedded',
            'unfocused': 'embedded'
            },
        pyatspi.ROLE_ENTRY: {
            'focused': 'labelOrName + placeholderText + readOnly + textRole + currentLineText + allTextSelection',
            'unfocused': 'labelOrName + placeholderText + readOnly + textRole + currentLineText + allTextSelection + ' + MNEMONIC,
            'basicWhereAmI': 'label + placeholderText + readOnly + textRole + textContent + anyTextSelection + ' + MNEMONIC,
            'detailedWhereAmI': 'label + placeholderText + readOnly + textRole + textContentWithAttributes + anyTextSelection + ' + MNEMONIC + ' + ' + TUTORIAL
            },
        pyatspi.ROLE_FRAME: {
            'focused': 'labelAndName + roleName',
            'unfocused': 'labelAndName + allTextSelection + roleName + unfocusedDialogCount + availability'
            },
        pyatspi.ROLE_HEADING: {
            'basicWhereAmI': 'label + readOnly + textRole + textContent + anyTextSelection + ' + MNEMONIC,
            'detailedWhereAmI': 'label + readOnly + textRole + textContentWithAttributes + anyTextSelection + ' + MNEMONIC + ' + ' + TUTORIAL
            },
        pyatspi.ROLE_ICON: {
            'focused': 'labelAndName + imageDescription + roleName + positionInList',
            'unfocused': 'labelAndName + imageDescription + roleName + positionInList',
            'basicWhereAmI': 'parentRoleName + labelAndName + selectedItemCount',
            'detailedWhereAmI': 'parentRoleName + labelAndName + selectedItemCount + selectedItems'
            },
        pyatspi.ROLE_LABEL: {
            'basicWhereAmI': 'labelAndName + allTextSelection + roleName'
            },
        pyatspi.ROLE_LAYERED_PANE: {
            'focused': 'labelAndName + allTextSelection + roleName + availability + noShowingChildren',
            'unfocused': 'labelAndName + allTextSelection + roleName + availability + noShowingChildren',
            'basicWhereAmI': 'labelAndName + roleName + selectedItemCount',
            'detailedWhereAmI': 'labelAndName + roleName + selectedItemCount + selectedItems'
            },
        pyatspi.ROLE_LINK: {
            'unfocused': 'labelAndName + roleName + availability + ' + MNEMONIC,
            'basicWhereAmI': 'linkInfo + siteDescription + fileSize + ' + MNEMONIC
            },
        pyatspi.ROLE_LIST: {
            'focused': 'focusedItem',
            'unfocused': 'labelOrName + focusedItem + multiselectableState + numberOfChildren'
            },
        pyatspi.ROLE_LIST_ITEM: {
            'focused': 'expandableState + availability',
            'unfocused': 'labelAndName + allTextSelection + expandableState + availability + positionInList + childWidget',
            'basicWhereAmI': 'label + roleName + name + positionInList + expandableState + (nodeLevel or nestingLevel)'
            },
        pyatspi.ROLE_MENU: {
            'focused': '[]',
            'unfocused': 'labelAndName + allTextSelection + roleName + availability + ' + MNEMONIC + ' + accelerator + positionInList',
            'basicWhereAmI': '(ancestors or parentRoleName) + labelAndName + roleName +  positionInList + ' + MNEMONIC
            },
        pyatspi.ROLE_MENU_ITEM: {
            'focused': 'expandableState',
            'unfocused': 'labelAndName + menuItemCheckedState + expandableState + availability + ' + MNEMONIC + ' + accelerator + positionInList',
            'basicWhereAmI': 'ancestors + labelAndName + accelerator + positionInList + ' + MNEMONIC
            },
        pyatspi.ROLE_NOTIFICATION: {
            'unfocused': 'roleName + unrelatedLabels'
            },
        pyatspi.ROLE_PAGE_TAB: {
            'focused': 'labelAndName + roleName + positionInList + ' + MNEMONIC + ' + accelerator',
            'unfocused': 'labelAndName + roleName + positionInList + ' + MNEMONIC + ' + accelerator',
            'basicWhereAmI': 'parentRoleName + labelAndName + roleName + positionInList + ' + MNEMONIC + ' + accelerator'
            },
        pyatspi.ROLE_PARAGRAPH: {
            'focused': 'labelOrName + readOnly + textRole + currentLineText + allTextSelection',
            'unfocused': 'labelOrName + readOnly + textRole + currentLineText + allTextSelection + ' + MNEMONIC,
            'basicWhereAmI': 'label + readOnly + textRole + textContent + anyTextSelection + ' + MNEMONIC,
            'detailedWhereAmI': 'label + readOnly + textRole + textContentWithAttributes + anyTextSelection + ' + MNEMONIC + ' + ' + TUTORIAL
            },
        pyatspi.ROLE_PASSWORD_TEXT: {
            'focused': 'labelOrName + readOnly + textRole + currentLineText + allTextSelection',
            'unfocused': 'labelOrName + readOnly + textRole + currentLineText + allTextSelection + ' + MNEMONIC,
            'basicWhereAmI': 'label + readOnly + textRole + textContent + anyTextSelection + ' + MNEMONIC,
            'detailedWhereAmI': 'label + readOnly + textRole + textContentWithAttributes + anyTextSelection + ' + MNEMONIC + ' + ' + TUTORIAL
            },
        pyatspi.ROLE_PROGRESS_BAR: {
            'focused': 'percentage',
            'unfocused': 'labelAndName + percentage'
            },
        pyatspi.ROLE_PUSH_BUTTON: {
            'focused': 'expandableState',
            'unfocused': 'labelAndName + expandableState + roleName + availability + ' + MNEMONIC + ' + accelerator',
            'basicWhereAmI': 'labelAndName + expandableState + roleName + ' + MNEMONIC + ' + accelerator'
            },
        pyatspi.ROLE_RADIO_BUTTON: {
            'focused': 'radioState',
            'unfocused': 'labelAndName + radioState + roleName + availability + ' + MNEMONIC + ' + accelerator + positionInList',
            'basicWhereAmI': 'radioButtonGroup + labelAndName + roleName + radioState + positionInGroup + ' + MNEMONIC + ' + accelerator'
            },
        pyatspi.ROLE_RADIO_MENU_ITEM: {
            # OpenOffice check menu items currently have a role of "menu item"
            # rather then "check menu item", so we need to test if one of the
            # states is CHECKED. If it is, then add that in to the list of
            # speech utterances. Note that we can't tell if this is a "check
            # menu item" that is currently unchecked and speak that state.
            # See Orca bug #433398 for more details.
            #
            'focused': 'labelAndName + radioState + roleName + availability + positionInList',
            'unfocused': 'labelAndName + radioState + roleName + availability + ' + MNEMONIC + ' + accelerator + positionInList',
            'basicWhereAmI': 'ancestors + labelAndName + roleName + radioState + accelerator + positionInList + ' + MNEMONIC
            },
        pyatspi.ROLE_SECTION: {
            'basicWhereAmI': 'label + readOnly + textRole + textContent + anyTextSelection + ' + MNEMONIC,
            'detailedWhereAmI': 'label + readOnly + textRole + textContentWithAttributes + anyTextSelection + ' + MNEMONIC + ' + ' + TUTORIAL
            },
        pyatspi.ROLE_SLIDER: {
            'focused': 'value',
            'unfocused': 'labelOrName + roleName + value + required + availability + ' + MNEMONIC,
            'basicWhereAmI': 'labelOrName + roleName + value + percentage + ' + MNEMONIC + ' + accelerator + required'
            },
        pyatspi.ROLE_SPIN_BUTTON: {
            'focused': 'name',
            'unfocused': 'labelAndName + allTextSelection + roleName + availability + ' + MNEMONIC + ' + required',
            'basicWhereAmI': 'label + roleName + name + allTextSelection + ' + MNEMONIC + ' + accelerator + required'
            },
        pyatspi.ROLE_SPLIT_PANE: {
            'focused': 'value',
            'unfocused': 'labelAndName + roleName + value + availability + ' + MNEMONIC,
            'basicWhereAmI' : 'labelAndName + roleName + value'
            },
        pyatspi.ROLE_TABLE: {
            'focused': 'labelAndName + table',
            'unfocused': 'labelAndName + table',
            'basicWhereAmI': 'labelAndName + table'
            },
        pyatspi.ROLE_TABLE_CELL: {
            'focused': '(tableCell2ChildLabel + tableCell2ChildToggle)\
                        or (cellCheckedState + (expandableState and (expandableState + numberOfChildren)))',
            'unfocused': 'tableCellRow',
            'basicWhereAmI': 'parentRoleName + columnHeader + rowHeader + roleName + cellCheckedState + (realActiveDescendantDisplayedText or imageDescription + image) + columnAndRow + expandableState + nodeLevel',
            'detailedWhereAmI': 'parentRoleName + columnHeader + rowHeader + roleName + cellCheckedState + (realActiveDescendantDisplayedText or imageDescription + image) + columnAndRow + tableCellRow + expandableState + nodeLevel'
            },
        'REAL_ROLE_TABLE_CELL': {
            # the real cell information
            # note that pyatspi.ROLE_TABLE_CELL is used to work out if we need to
            # read a whole row. It calls REAL_ROLE_TABLE_CELL internally.
            # maybe it can be done in a cleaner way?
            #
            'focused':   '(tableCell2ChildLabel + tableCell2ChildToggle)\
                          or (cellCheckedState + (expandableState and (expandableState + numberOfChildren)))',
            'unfocused': '(tableCell2ChildLabel + tableCell2ChildToggle)\
                          or (columnHeaderIfToggleAndNoText\
                              + cellCheckedState\
                              + (realActiveDescendantDisplayedText or imageDescription + image)\
                              + (expandableState and (expandableState + numberOfChildren))\
                              + required)'
            },
        pyatspi.ROLE_TEAROFF_MENU_ITEM: {
            'focused': '[]',
            'unfocused': 'labelAndName + allTextSelection + roleName + availability '
            },
        pyatspi.ROLE_TERMINAL: {
            'focused': 'terminal',
            'unfocused': 'terminal',
            'basicWhereAmI': 'label + readOnly + textRole + textContent + anyTextSelection + ' + MNEMONIC,
            'detailedWhereAmI': 'label + readOnly + textRole + textContentWithAttributes + anyTextSelection + ' + MNEMONIC + ' + ' + TUTORIAL
            },
        pyatspi.ROLE_TEXT: {
            'focused': 'labelOrName + placeholderText + readOnly + textRole + textIndentation + currentLineText + allTextSelection',
            'unfocused': 'labelOrName + placeholderText + readOnly + textRole + textIndentation + currentLineText + allTextSelection + ' + MNEMONIC,
            'basicWhereAmI': 'label + placeholderText + readOnly + textRole + textContent + anyTextSelection + ' + MNEMONIC,
            'detailedWhereAmI': 'label + placeholderText + readOnly + textRole + textContentWithAttributes + anyTextSelection + ' + MNEMONIC + ' + ' + TUTORIAL
            },
        pyatspi.ROLE_TOGGLE_BUTTON: {
            'focused': 'expandableState or toggleState',
            'unfocused': 'labelAndName + roleName + (expandableState or toggleState) + availability + ' + MNEMONIC + ' + accelerator',
            'basicWhereAmI': 'labelAndName + roleName + (expandableState or toggleState)'
            },
        pyatspi.ROLE_TOOL_TIP: {
            'unfocused': 'labelAndName',
            'basicWhereAmI': 'labelAndName'
            },
    }
    }
