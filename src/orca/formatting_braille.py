import pyatspi
from formatting_consts import BRAILLE_TEXT

def braille():

    return {
        'braille': {
        'prefix': {
#            'focused':   'ancestors\
#                         + (rowHeader and [Region(" " + asString(rowHeader))])\
#                         + (columnHeader and [Region(" " + asString(columnHeader))])\
#                         + (radioButtonGroup and [Region(" " + asString(radioButtonGroup))])\
#                         + [Region(" ")]',
#            'unfocused': 'ancestors\
#                         + (rowHeader and [Region(" " + asString(rowHeader))])\
#                         + (columnHeader and [Region(" " + asString(columnHeader))])\
#                         + (radioButtonGroup and [Region(" " + asString(radioButtonGroup))])\
#                         + [Region(" ")]',
            'focused':   '(includeContext\
                           and (ancestors\
                                + (rowHeader and [Region(" " + asString(rowHeader))])\
                                + (columnHeader and [Region(" " + asString(columnHeader))])\
                                + (radioButtonGroup and [Region(" " + asString(radioButtonGroup))])\
                                + [Region(" ")])\
                           or [])',
            'unfocused': '(includeContext\
                           and (ancestors\
                                + (rowHeader and [Region(" " + asString(rowHeader))])\
                                + (columnHeader and [Region(" " + asString(columnHeader))])\
                                + (radioButtonGroup and [Region(" " + asString(radioButtonGroup))])\
                                + [Region(" ")])\
                           or [])',
            },
        'suffix': {
            'focused':   '(nodeLevel and [Region(" " + asString(nodeLevel))])',
            'unfocused': '(nodeLevel and [Region(" " + asString(nodeLevel))])',
            },
        'default': {
            'focused':   '[Component(obj,\
                                     asString(label + displayedText + value + roleName + required))]',
            'unfocused': '[Component(obj,\
                                     asString(label + displayedText + value + roleName + required))]',
            },
        #pyatspi.ROLE_ALERT: 'default'
        pyatspi.ROLE_ANIMATION: {
            'unfocused': '[Component(obj,\
                                     asString(label + displayedText + roleName + (description and space(": ") + description)))]',
            },
        #pyatspi.ROLE_ARROW: 'default'
        pyatspi.ROLE_CANVAS: {
            'unfocused': '[Component(obj,\
                                     asString(((label + displayedText + imageDescription) or name) + roleName))]'
            },
        pyatspi.ROLE_CHECK_BOX: {
            'unfocused': '[Component(obj,\
                                     asString(label + displayedText + roleName),\
                                     indicator=asString(checkedState))]'
            },
        pyatspi.ROLE_CHECK_MENU_ITEM: {
            'unfocused': '[Component(obj,\
                                     asString(label + displayedText + roleName + availability) + asString(accelerator),\
                                     indicator=asString(checkedState))]'
            },
        #pyatspi.ROLE_COLUMN_HEADER: 'default'
        pyatspi.ROLE_COMBO_BOX: {
            # [[[TODO: WDW - maybe pass the label into the region constructor?
            # We could then use the cursorOffset field to indicate where the
            # combobox starts.]]]
            #
            'unfocused': '((comboBoxTextObj and [Text(comboBoxTextObj[0], asString(label), asString(eol))])\
                           or [Component(obj, asString(label + displayedText), label and (len(asString(label)) + 1) or 0)])\
                          + [Region(" " + asString(roleName))]'
            },
        #pyatspi.ROLE_DESKTOP_ICON: 'default'
        #pyatspi.ROLE_DIAL: 'default'
        #pyatspi.ROLE_DIALOG: 'default'
        #pyatspi.ROLE_DIRECTORY_PANE: 'default'
        pyatspi.ROLE_EMBEDDED: {
            'unfocused': '[Component(obj,\
                                     asString(label + displayedText) or asString(applicationName))]'
            },
        pyatspi.ROLE_ENTRY: {
            'unfocused': BRAILLE_TEXT
            },
        pyatspi.ROLE_FRAME: {
            'focused':   '[Component(obj,\
                                     asString(((label + displayedText) or name) + value + roleName + alertAndDialogCount))]',
            'unfocused': '[Component(obj,\
                                     asString(((label + displayedText) or name) + value + roleName + alertAndDialogCount))]'
            },
        pyatspi.ROLE_HEADING: {
            'unfocused': '[Text(obj)] + [Region(" " + asString(roleName))]'
            },
        #pyatspi.ROLE_HTML_CONTAINER: 'default'
        pyatspi.ROLE_ICON: {
            'unfocused': '[Component(obj,\
                                     asString(((label + displayedText + imageDescription) or name) + roleName))]'
            },
        pyatspi.ROLE_IMAGE: {
            'focused':   '[Component(obj,\
                                     asString(labelAndName + value + roleName + required))]',
            'unfocused': '[Component(obj,\
                                     asString(labelAndName + value + roleName + required))]',
            },
        pyatspi.ROLE_LABEL: {
            'unfocused': '[Text(obj,\
                                asString(label),\
                                asString(eol))]'
            },
        pyatspi.ROLE_LINK: {
            'unfocused': '[Link(obj, asString(currentLineText)\
                                     or asString(displayedText)\
                                     or asString(name))]',
        },
        pyatspi.ROLE_LIST: {
            'unfocused': '[Component(obj,\
                                     asString(label + focusedItem + roleName),\
                                     asString(label) and (len(asString(label)) + 1) or 0)]'
        },
        pyatspi.ROLE_LIST_ITEM: {
            'focused':   '[Component(obj,\
                                     asString(label + displayedText + expandableState + roleName + availability) + asString(accelerator))]\
                          + (nestingLevel and [Region(" " + asString(nestingLevel))])\
                          + (childWidget and ([Region(" ")] + childWidget))',
            'unfocused': '[Component(obj,\
                                     asString(label + displayedText + expandableState))]\
                          + (nestingLevel and [Region(" " + asString(nestingLevel))])\
                          + (childWidget and ([Region(" ")] + childWidget))',
            },
        pyatspi.ROLE_MENU: {
            'focused':   '[Component(obj,\
                                     asString(label + displayedText + roleName + availability) + asString(accelerator))]',
            'unfocused': '[Component(obj,\
                                     asString(label + displayedText + roleName))]',
            },
        #pyatspi.ROLE_MENU_BAR: 'default'
        pyatspi.ROLE_MENU_ITEM: {
            'unfocused': '[Component(obj,\
                                     asString(label + displayedText + expandableState + availability) + asString(accelerator),\
                                     indicator=asString(menuItemCheckedState))]'
            },
        #pyatspi.ROLE_OPTION_PANE: 'default'
        pyatspi.ROLE_PAGE_TAB: {
            'focused':   '[Component(obj,\
                                     asString(label + displayedText + roleName + availability) + asString(accelerator))]',
            'unfocused': '[Component(obj,\
                                     asString(label + displayedText + roleName))]'
            },
        #pyatspi.ROLE_PAGE_TAB_LIST: 'default'
        pyatspi.ROLE_PANEL: {
            'unfocused': '[Component(obj,\
                                     asString((label or displayedText) + roleName))]\
                          + (childWidget and ([Region(" ")] + childWidget))'
            },
        pyatspi.ROLE_PARAGRAPH: {
            'unfocused': BRAILLE_TEXT
            },
        pyatspi.ROLE_PASSWORD_TEXT: {
            'unfocused': BRAILLE_TEXT
            },
        #pyatspi.ROLE_PROGRESS_BAR: 'default'
        pyatspi.ROLE_PUSH_BUTTON: {
            'unfocused': '[Component(obj,\
                                     asString(((label + displayedText) or description) + expandableState + roleName))]'
            },
        pyatspi.ROLE_RADIO_BUTTON: {
            'unfocused': '[Component(obj,\
                                     asString(((label + displayedText) or description) + roleName),\
                                     indicator=asString(radioState))]'
            },
        pyatspi.ROLE_RADIO_MENU_ITEM: {
            'focused':   '[Component(obj,\
                                     asString(((label + displayedText) or description) + roleName + availability)\
                                     + asString(accelerator),\
                                     indicator=asString(radioState))]',
            'unfocused': '[Component(obj,\
                                     asString((label + displayedText) or description)\
                                     + asString(accelerator),\
                                     indicator=asString(radioState))]'
            },
        #pyatspi.ROLE_ROW_HEADER: 'default'
        #pyatspi.ROLE_SCROLL_BAR: 'default'
        pyatspi.ROLE_SCROLL_PANE: {
            'unfocused': 'asPageTabOrScrollPane'
            },
        #'REAL_ROLE_SCROLL_PANE': 'default'
        pyatspi.ROLE_SLIDER: {
            'unfocused': '[Component(obj,\
                                     asString(labelOrName + value + roleName + required))]'
            },
        pyatspi.ROLE_SPIN_BUTTON: {
            'unfocused': '[Text(obj, asString(label), asString(eol))]\
                          + (required and [Region(" " + asString(required))] or [])\
                          + (readOnly and [Region(" " + asString(readOnly))] or [])'
            },
        #pyatspi.ROLE_SPLIT_PANE: 'default'
        #pyatspi.ROLE_TABLE: 'default'
        pyatspi.ROLE_TABLE_CELL: {
            'unfocused': 'tableCellRow',
            },
        'REAL_ROLE_TABLE_CELL': {
            'unfocused': '(tableCell2ChildToggle + tableCell2ChildLabel)\
                          or (cellCheckedState\
                              + (columnHeaderIfToggleAndNoText and [Region(" "), Component(obj, asString(columnHeaderIfToggleAndNoText))])\
                              + ((realActiveDescendantDisplayedText and [Component(obj, asString(realActiveDescendantDisplayedText))])\
                                 or (imageDescription and [Region(" "), Component(obj, asString(imageDescription))]))\
                              + (realActiveDescendantRoleName and [Component(obj, (realActiveDescendantDisplayedText and " " or "") + asString(realActiveDescendantRoleName))])\
                              + (expandableState and [Region(" " + asString(expandableState))])\
                              + (required and [Region(" " + asString(required))]))\
                          or ([Component(obj,"")])'
            },
        #pyatspi.ROLE_TABLE_COLUMN_HEADER: 'default'
        #pyatspi.ROLE_TABLE_ROW_HEADER: 'default'
        pyatspi.ROLE_TEAROFF_MENU_ITEM: {
            'unfocused': '[Component(obj,\
                                     asString(roleName))]'
            },
        pyatspi.ROLE_TERMINAL: {
            'unfocused': '[Text(obj)]'
            },
        pyatspi.ROLE_TEXT: {
            'unfocused': BRAILLE_TEXT
            },
        pyatspi.ROLE_TOGGLE_BUTTON: {
            'unfocused': '[Component(obj,\
                                     asString(((label + displayedText) or description) + expandableState + roleName),\
                                     indicator=asString(toggleState))]'
            },
        #pyatspi.ROLE_TOOL_BAR: 'default'
        #pyatspi.ROLE_TREE: 'default'
        #pyatspi.ROLE_TREE_TABLE: 'default'
        #pyatspi.ROLE_WINDOW: 'default'
        }
    }

import pprint
pprint.pprint(braille())
