import pyatspi
from . import object_properties
from . import settings
from formatting_const import PAUSE_STR
from formatting_const import TUTORIAL_STR 
from formatting_const import TUTORIAL 
from formatting_const import MNEMONIC
from formatting_const import BRAILLE_TEXT
from formatting_const import _add
from formatting_const import _or
from formatting_const import _grp

def create_formating():
    formatting = { 
    'strings': { 

	'speech': { 

            'required': object_properties.STATE_REQUIRED_SPEECH, 
            'readonly': object_properties.STATE_READ_ONLY_SPEECH, 
            'insensitive': object_properties.STATE_INSENSITIVE_SPEECH, 
            'checkbox': object_properties.CHECK_BOX_INDICATORS_SPEECH, 
            'radiobutton': object_properties.RADIO_BUTTON_INDICATORS_SPEECH, 
            'togglebutton': object_properties.TOGGLE_BUTTON_INDICATORS_SPEECH, 
            'expansion': object_properties.EXPANSION_INDICATORS_SPEECH, 
            'nodelevel': object_properties.NODE_LEVEL_SPEECH, 
            'nestinglevel': object_properties.NESTING_LEVEL_SPEECH,
            'multiselect': object_properties.STATE_MULTISELECT_SPEECH, 
            'iconindex':object_properties.ICON_INDEX_SPEECH, 
            'groupindex': object_properties.GROUP_INDEX_SPEECH, 
        }, 
        'braille': { 

            'eol': settings.brailleEOLIndicator,
            'required': object_properties.STATE_REQUIRED_BRAILLE, 
            'readonly':	object_properties.STATE_READ_ONLY_BRAILLE, 
            'insensitive': object_properties.STATE_INSENSITIVE_BRAILLE, 
            'checkbox': object_properties.CHECK_BOX_INDICATORS_BRAILLE, 
            'radiobutton': object_properties.RADIO_BUTTON_INDICATORS_BRAILLE, 
            'togglebutton': object_properties.TOGGLE_BUTTON_INDICATORS_BRAILLE, 
            'expansion': object_properties.EXPANSION_INDICATORS_BRAILLE, 
            'nodelevel': object_properties.NODE_LEVEL_BRAILLE, 
            'nestinglevel': object_properties.NESTING_LEVEL_BRAILLE, 
        }, 
    }, 

    'speech': { 

        'prefix': { 

            'focused': '[]',
            'unfocused': 'oldAncestors + newAncestors + newRowHeader + newColumnHeader + newRadioButtonGroup',
            'basicWhereAmI': 'toolbar', 
            'detailedWhereAmI': '[]' 
        }, 
        'suffix': {
            'focused': '[]', 
            'unfocused': 'newNodeLevel + unselectedCell + ' +
            TUTORIAL, 
            'basicWhereAmI': TUTORIAL + ' + description', 
            'detailedWhereAmI': '[]' 
        }, 
        'default': { 
            'focused': '[]', 
            'unfocused': 'labelAndName + allTextSelection + roleName + availability + ' + MNEMONIC
            + ' + accelerator + childWidget', 
            'basicWhereAmI':                     'labelAndName + roleName', 
            'detailedWhereAmI': '[]' 
        }, 
        pyatspi.ROLE_ALERT:	{ 
            'unfocused': 'labelAndName + unrelatedLabels' 
        }, 
        pyatspi.ROLE_ANIMATION:{ 
            'unfocused': 'labelAndName' 
        }, 
        pyatspi.ROLE_CANVAS: { 

            'focused' :  'labelAndName + imageDescription + roleName + positionInList', 
            'unfocused' : 'labelAndName + imageDescription + roleName + positionInList',
            'basicWhereAmI': 'parentRoleName + labelAndName + selectedItemCount',
            'detailedWhereAmI':  'parentRoleName + labelAndName + selectedItemCount + selectedItems' 
        },
	pyatspi.ROLE_CHECK_BOX: { 

            'focused': 'checkedState', 
            'unfocused': 'labelAndName + roleName + checkedState + required + availability + ' +
            MNEMONIC + ' + accelerator', 
            'basicWhereAmI': 'namedContainingPanel + labelAndName + roleName + checkedState + ' +
            MNEMONIC + ' + accelerator + required' 
        }, 
        pyatspi.ROLE_CHECK_MENU_ITEM: {
            'focused': 'checkedState', 
            'unfocused': 'labelAndName + roleName + checkedState + required + availability + ' +
            MNEMONIC + ' + accelerator + positionInList',
            'basicWhereAmI':            plus(
                'ancestors',
                'labelAndName',
                'roleName',
                'checkedState',
                'accelerator',
                'positionInList',
                MNEMONIC )
        }, 

        pyatspi.ROLE_COLOR_CHOOSER: { 

            'focused': 'value',
            'unfocused': 'label + roleName + value + required + availability + ' +  MNEMONIC, 
            'basicWhereAmI': 'label + roleName + value + percentage + ' + MNEMONIC + ' + accelerator + required' 
        }, 

        pyatspi.ROLE_COMBO_BOX: {
            'focused': 'name + positionInList', 
            'unfocused': 'label + name + roleName + positionInList + ' + MNEMONIC +         ' + accelerator', 
            'basicWhereAmI': 'label + roleName + name + positionInList + ' + MNEMONIC +        ' + accelerator' 
        }, 

        pyatspi.ROLE_DIALOG: { 

            'unfocused': 'labelAndName + unrelatedLabels' 
        }, 

        pyatspi.ROLE_DOCUMENT_FRAME: {
            'basicWhereAmI': 'label + readOnly + textRole + textContent + anyTextSelection + ' +
            MNEMONIC, 
            'detailedWhereAmI':            plus(
                'label' ,
                'readOnly' ,
                'textRole' ,
                'textContentWithAttributes' ,
                'anyTextSelection' ,
                'MNEMONIC' ,
                TUTORIAL )
        }, 

        pyatspi.ROLE_EMBEDDED: { 

            'focused': 'embedded', 
            'unfocused': 'embedded' 
        }, 
        
        pyatspi.ROLE_ENTRY: { 

            'focused': 'labelOrName + placeholderText + readOnly + textRole + currentLineText + allTextSelection',
            'unfocused': 'labelOrName + placeholderText + readOnly + textRole + currentLineText + allTextSelection + ' + MNEMONIC, 
            'basicWhereAmI': 'label + placeholderText + readOnly + textRole + textContent + anyTextSelection + '+ MNEMONIC, 
            'detailedWhereAmI': 'label + placeholderText + readOnly + textRole + textContentWithAttributes + anyTextSelection + ' + MNEMONIC + ' + ' + TUTORIAL }, 
        pyatspi.ROLE_FRAME: {
            'focused':            'labelAndName + roleName', 
            'unfocused': 'labelAndName + allTextSelection + roleName + unfocusedDialogCount + availability'
        }, 
        pyatspi.ROLE_HEADING: { 

            'basicWhereAmI': 'label + readOnly + textRole + textContent + anyTextSelection + ' +	MNEMONIC, 
            'detailedWhereAmI': 'label + readOnly + textRole + textContentWithAttributes + anyTextSelection + '	+ MNEMONIC + ' + ' + TUTORIAL }, 
        pyatspi.ROLE_ICON: { 

            'focused':'labelAndName + imageDescription + roleName + positionInList', 
            'unfocused' : 'labelAndName + imageDescription + roleName + positionInList',
            'basicWhereAmI': 'parentRoleName + labelAndName + selectedItemCount',
            'detailedWhereAmI':	'parentRoleName + labelAndName + selectedItemCount + selectedItems' },
        pyatspi.ROLE_LABEL: {
            'basicWhereAmI': 'labelAndName + allTextSelection + roleName' }, 
        pyatspi.ROLE_LAYERED_PANE:	{ 
            'focused': 'labelAndName + allTextSelection + roleName + availability + noShowingChildren',
            'unfocused': 'labelAndName + allTextSelection + roleName + availability + noShowingChildren',
            'basicWhereAmI': 'labelAndName + roleName + selectedItemCount',
            'detailedWhereAmI':	'labelAndName + roleName + selectedItemCount + selectedItems' }, 
        pyatspi.ROLE_LINK: { 

	'unfocused': 'labelAndName + roleName + availability + ' +	MNEMONIC, 
            'basicWhereAmI': 'linkInfo + siteDescription + fileSize + ' +	MNEMONIC }, 
        pyatspi.ROLE_LIST: { 

	'focused': 'focusedItem', 
            'unfocused':	'labelOrName + focusedItem + multiselectableState + numberOfChildren' },
        pyatspi.ROLE_LIST_ITEM: { 

	'focused': 'expandableState + availability',
            'unfocused': 'labelAndName + allTextSelection + expandableState + availability + positionInList + childWidget',
            'basicWhereAmI': 'label + roleName + name + positionInList + expandableState + (nodeLevel or nestingLevel)'
        }, 
                   pyatspi.ROLE_MENU: { 

	'focused': '[]', 
                       'unfocused':	'labelAndName + allTextSelection + roleName + availability + ' + MNEMONIC
                       + ' + accelerator + positionInList', 
                       'basicWhereAmI': '(ancestors or parentRoleName) + labelAndName + roleName +  positionInList + '	+ MNEMONIC }, 
        pyatspi.ROLE_MENU_ITEM: {
            'focused': 'expandableState',
            'unfocused':	'labelAndName + menuItemCheckedState + expandableState + availability + '	+ MNEMONIC + ' + accelerator + positionInList', 
            'basicWhereAmI': 'ancestors + labelAndName + accelerator + positionInList + ' + MNEMONIC },
        pyatspi.ROLE_NOTIFICATION: { 

	'unfocused': 'roleName + unrelatedLabels' },
        pyatspi.ROLE_PAGE_TAB: { 

	'focused':	'labelAndName + roleName + positionInList + ' + MNEMONIC +
            ' + accelerator', 
            'unfocused':	'labelAndName + roleName + positionInList + ' + MNEMONIC +
            ' + accelerator', 
            'basicWhereAmI': 'parentRoleName + labelAndName + roleName + positionInList + ' + MNEMONIC
            + ' + accelerator' }, 
        pyatspi.ROLE_PARAGRAPH: { 

	'focused':	'labelOrName + readOnly + textRole + currentLineText + allTextSelection',
            'unfocused': 'labelOrName + readOnly + textRole + currentLineText + allTextSelection + '	+ MNEMONIC, 
            'basicWhereAmI': 'label + readOnly + textRole + textContent + anyTextSelection + ' +	MNEMONIC, 
            'detailedWhereAmI': 'label + readOnly + textRole + textContentWithAttributes + anyTextSelection + '	+ MNEMONIC + ' + ' + TUTORIAL }, 
        pyatspi.ROLE_PASSWORD_TEXT: { 

	'focused':	'labelOrName + readOnly + textRole + currentLineText + allTextSelection',
            'unfocused': 'labelOrName + readOnly + textRole + currentLineText + allTextSelection + '	+ MNEMONIC, 
            'basicWhereAmI': 'label + readOnly + textRole + textContent + anyTextSelection + ' +	MNEMONIC, 
            'detailedWhereAmI': 'label + readOnly + textRole + textContentWithAttributes + anyTextSelection + '	+ MNEMONIC + ' + ' + TUTORIAL }, 
        pyatspi.ROLE_PROGRESS_BAR: { 

	'focused':	'percentage', 
            'unfocused': 'labelAndName + percentage' }, 
        pyatspi.ROLE_PUSH_BUTTON: { 
            'focused': 'expandableState', 
            'unfocused':	'labelAndName + expandableState + roleName + availability + ' + MNEMONIC +
            ' + accelerator', 
            'basicWhereAmI': 'labelAndName + expandableState + roleName + ' + MNEMONIC +
            ' + accelerator' }, 
        pyatspi.ROLE_RADIO_BUTTON: { 
            'focused': 'radioState',
            'unfocused': 'labelAndName + radioState + roleName + availability + ' +	MNEMONIC + ' + accelerator + positionInList', 
            'basicWhereAmI': 'radioButtonGroup + labelAndName + roleName + radioState + positionInGroup + '	+ MNEMONIC + ' + accelerator' }, 
        pyatspi.ROLE_RADIO_MENU_ITEM: { 
            'focused'
            : 'labelAndName + radioState + roleName + availability + positionInList',
            'unfocused': 'labelAndName + radioState + roleName + availability + ' +	MNEMONIC + ' + accelerator + positionInList', 
            'basicWhereAmI': 'ancestors + labelAndName + roleName + radioState + accelerator + positionInList + '	+ MNEMONIC }, 
        pyatspi.ROLE_SECTION: { 
            'basicWhereAmI': 'label + readOnly + textRole + textContent + anyTextSelection + ' +	MNEMONIC, 
            'detailedWhereAmI': 'label + readOnly + textRole + textContentWithAttributes + anyTextSelection + '	+ MNEMONIC + ' + ' + TUTORIAL }, 
        pyatspi.ROLE_SLIDER: { 
            'focused':	'value', 
            'unfocused':	'labelOrName + roleName + value + required + availability + ' + MNEMONIC,
            'basicWhereAmI': 'labelOrName + roleName + value + percentage + ' +	MNEMONIC + ' + accelerator + required' }, 
        pyatspi.ROLE_SPIN_BUTTON: {
            'focused': 'name', 
            'unfocused':	'labelAndName + allTextSelection + roleName + availability + ' + MNEMONIC
            + ' + required', 
            'basicWhereAmI': 'label + roleName + name + allTextSelection + ' + MNEMONIC +
            ' + accelerator + required' }, 
        pyatspi.ROLE_SPLIT_PANE: { 
            'focused':	'value', 
            'unfocused': 'labelAndName + roleName + value + availability + '	+ MNEMONIC, 
            'basicWhereAmI': 'labelAndName + roleName + value' }, 
        pyatspi.ROLE_TABLE: { 
            'focused': 'labelAndName + table', 
            'unfocused':	'labelAndName + table', 
            'basicWhereAmI': 'labelAndName + table' }, pyatspi
        .ROLE_TABLE_CELL: { 
            'focused': '(tableCell2ChildLabel + tableCell2ChildToggle)            or (cellCheckedState + (expandableState and (expandableState + numberOfChildren)))',
            'unfocused': 'tableCellRow', 
            'basicWhereAmI': 'parentRoleName + columnHeader + rowHeader + roleName + cellCheckedState + (realActiveDescendantDisplayedText or imageDescription + image) + columnAndRow + expandableState + nodeLevel',
            'detailedWhereAmI': 'parentRoleName + columnHeader + rowHeader + roleName + cellCheckedState + (realActiveDescendantDisplayedText or imageDescription + image) + columnAndRow + tableCellRow + expandableState + nodeLevel'
        }, 
            'REAL_ROLE_TABLE_CELL': { 
                'focused': '(tableCell2ChildLabel + tableCell2ChildToggle)or (cellCheckedState + (expandableState and (expandableState + numberOfChildren)))',
                'unfocused': '(tableCell2ChildLabel + tableCell2ChildToggle)or (columnHeaderIfToggleAndNoText    + cellCheckedState    + (realActiveDescendantDisplayedText or imageDescription + image)    + (expandableState and (expandableState + numberOfChildren))    + required)'
            }, 
                   pyatspi.ROLE_TEAROFF_MENU_ITEM: {
                       'focused': '[]', 
                       'unfocused': 'labelAndName + allTextSelection + roleName + availability ' 
                   }, 
                   pyatspi.ROLE_TERMINAL: { 

                       'focused': 'terminal', 
                       'unfocused': 'terminal',
                       'basicWhereAmI': 'label + readOnly + textRole + textContent + anyTextSelection + ' +	MNEMONIC, 
                       'detailedWhereAmI': 'label + readOnly + textRole + textContentWithAttributes + anyTextSelection + '	+ MNEMONIC + ' + ' + TUTORIAL }, 

        pyatspi.ROLE_TEXT: 
        { 
            'focused': 'labelOrName + placeholderText + readOnly + textRole + textIndentation + currentLineText + allTextSelection',
            'unfocused': 'labelOrName + placeholderText + readOnly + textRole + textIndentation + currentLineText + allTextSelection + '
            + MNEMONIC, 
            'basicWhereAmI': 'label + placeholderText + readOnly + textRole + textContent + anyTextSelection + '
            + MNEMONIC, 
            'detailedWhereAmI': 'label + placeholderText + readOnly + textRole + textContentWithAttributes + anyTextSelection + '
            + MNEMONIC + ' + ' + TUTORIAL }, 
        pyatspi.ROLE_TOGGLE_BUTTON: { 

            'focused': 'expandableState or toggleState', 
            'unfocused': 'labelAndName + roleName + (expandableState or toggleState) + availability + '
            + MNEMONIC + ' + accelerator', 
            'basicWhereAmI': 'labelAndName + roleName + (expandableState or toggleState)' }, 
        pyatspi.ROLE_TOOL_TIP: { 

            'unfocused': 'labelAndName', 
            'basicWhereAmI': 'labelAndName' 
        }, 
    }, 
    'braille': { 

        'prefix': { 

            'focused':            (
                '(includeContext'
                'and (ancestors'
                '+ (rowHeader and [Region(" " + asString(rowHeader))])'
                '+ (columnHeader and [Region(" " + asString(columnHeader))])'
                '+ (radioButtonGroup and [Region(" " + asString(radioButtonGroup))])'
                '+ [Region(" ")])'
                'or [])')
            ,
            'unfocused': '(includeContext and (ancestors      + (rowHeader and [Region(" " + asString(rowHeader))])      + (columnHeader and [Region(" " + asString(columnHeader))])      + (radioButtonGroup and [Region(" " + asString(radioButtonGroup))])      + [Region(" ")]) or [])',
        }, 
            'suffix': { 
                'focused':	'(nodeLevel and [Region(" " + asString(nodeLevel))])', 
                'unfocused':	'(nodeLevel and [Region(" " + asString(nodeLevel))])', }, 
        'default': {
            'focused': '[Component(obj,           asString(label + displayedText + value + roleName + required))]',
            'unfocused': '[Component(obj,           asString(label + displayedText + value + roleName + required))]',
        }, 
                   pyatspi.ROLE_ANIMATION: { 
                       'unfocused': '[Component(obj,           asString(label + displayedText + roleName + (description and space(": ") + description)))]',
                   }, 
                   pyatspi.ROLE_CANVAS: { 
                       'unfocused': '[Component(obj,           asString(((label + displayedText + imageDescription) or name) + roleName))]'
                   }, 
                   pyatspi.ROLE_CHECK_BOX: { 

                       'unfocused': '[Component(obj,           asString(label + displayedText + roleName),           indicator=asString(checkedState))]'
                   }, 
                   pyatspi.ROLE_CHECK_MENU_ITEM: { 
                       'unfocused': '[Component(obj,           asString(label + displayedText + roleName + availability) + asString(accelerator),           indicator=asString(checkedState))]'
                   }, 
                   pyatspi.ROLE_COMBO_BOX: { 
                       'unfocused': '((comboBoxTextObj and [Text(comboBoxTextObj[0], asString(label), asString(eol))]) or [Component(obj, asString(label + displayedText), label and (len(asString(label)) + 1) or 0)])+ [Region(" " + asString(roleName))]'
                   }, 
                   pyatspi.ROLE_EMBEDDED: { 
                       'unfocused': '[Component(obj,           asString(label + displayedText) or asString(applicationName))]'
                   }, 
                   pyatspi.ROLE_ENTRY: { 

                       'unfocused': BRAILLE_TEXT 
                   }, 
                   pyatspi.ROLE_FRAME:	{ 'focused': '[Component(obj,           asString(((label + displayedText) or name) + value + roleName + alertAndDialogCount))]',
                                          'unfocused': '[Component(obj,           asString(((label + displayedText) or name) + value + roleName + alertAndDialogCount))]'
                                      }, 
                   pyatspi.ROLE_HEADING: {
                       'unfocused': 	'[Text(obj)] + [Region(" " + asString(roleName))]' 
                   }, 
                   pyatspi.ROLE_ICON: {
                       'unfocused': '[Component(obj,           asString(((label + displayedText + imageDescription) or name) + roleName))]'
                   }, 
                   pyatspi.ROLE_IMAGE: { 
                       'focused': '[Component(obj,           asString(labelAndName + value + roleName + required))]',
                       'unfocused': '[Component(obj,           asString(labelAndName + value + roleName + required))]',
                   }, 
                   pyatspi.ROLE_LABEL: { 
                       'unfocused': '[Text(obj,      asString(label),      asString(eol))]'
                   }, 
                   pyatspi.ROLE_LINK: { 
                       'unfocused': '[Link(obj, asString(currentLineText)           or asString(displayedText)           or asString(name))]',
                   }, 
                   pyatspi.ROLE_LIST: { 
                       'unfocused': '[Component(obj,           asString(label + focusedItem + roleName),           asString(label) and (len(asString(label)) + 1) or 0)]'
                   }, 
                   pyatspi.ROLE_LIST_ITEM: { 
                       'focused': '[Component(obj,           asString(label + displayedText + expandableState + roleName + availability) + asString(accelerator))]+ (nestingLevel and [Region(" " + asString(nestingLevel))])+ (childWidget and ([Region(" ")] + childWidget))',
                       'unfocused': '[Component(obj,           asString(label + displayedText + expandableState))]+ (nestingLevel and [Region(" " + asString(nestingLevel))])+ (childWidget and ([Region(" ")] + childWidget))',
                   }, 
                   pyatspi.ROLE_MENU: { 
                       'focused': '[Component(obj,           asString(label + displayedText + roleName + availability) + asString(accelerator))]',
                       'unfocused': '[Component(obj,           asString(label + displayedText + roleName))]',
                   }, 
                   pyatspi.ROLE_MENU_ITEM: { 
                       'unfocused': '[Component(obj,           asString(label + displayedText + expandableState + availability) + asString(accelerator),           indicator=asString(menuItemCheckedState))]'
                   }, 
                   pyatspi.ROLE_PAGE_TAB: { 
                       'focused': '[Component(obj,           asString(label + displayedText + roleName + availability) + asString(accelerator))]',
                       'unfocused': '[Component(obj,           asString(label + displayedText + roleName))]'
                   }, 
                   pyatspi.ROLE_PANEL: { 
                       'unfocused': '[Component(obj,           asString((label or displayedText) + roleName))]+ (childWidget and ([Region(" ")] + childWidget))'
                   }, 
                   pyatspi.ROLE_PARAGRAPH: { 
                       'unfocused': BRAILLE_TEXT }, 
                   pyatspi.ROLE_PASSWORD_TEXT: { 
                       'unfocused': BRAILLE_TEXT }, 
                   pyatspi.ROLE_PUSH_BUTTON: { 
                       'unfocused': '[Component(obj,           asString(((label + displayedText) or description) + expandableState + roleName))]'
                   }, 
                   pyatspi.ROLE_RADIO_BUTTON: { 
                       'unfocused': '[Component(obj,           asString(((label + displayedText) or description) + roleName),           indicator=asString(radioState))]'
                   }, 
                   pyatspi.ROLE_RADIO_MENU_ITEM: { 
                       'focused': '[Component(obj,           asString(((label + displayedText) or description) + roleName + availability)           + asString(accelerator),           indicator=asString(radioState))]',
                       'unfocused': '[Component(obj,           asString((label + displayedText) or description)           + asString(accelerator),           indicator=asString(radioState))]'
                   }, 
        pyatspi.ROLE_SCROLL_PANE: { 
            'unfocused': 'asPageTabOrScrollPane' },
        pyatspi.ROLE_SLIDER: { 
            'unfocused': '[Component(obj,           asString(labelOrName + value + roleName + required))]'
        }, 
        pyatspi.ROLE_SPIN_BUTTON: { 
            'unfocused': '[Text(obj, asString(label), asString(eol))]      + (required and [Region(" " + asString(required))] or [])    + (readOnly and [Region(" " + asString(readOnly))] or [])'
        }, 
                   pyatspi.ROLE_TABLE_CELL: { 
                       'unfocused': 'tableCellRow', },
                   'REAL_ROLE_TABLE_CELL': { 
                       'unfocused': '(tableCell2ChildToggle + tableCell2ChildLabel)or (cellCheckedState    + (columnHeaderIfToggleAndNoText and [Region(" "), Component(obj, asString(columnHeaderIfToggleAndNoText))])    + ((realActiveDescendantDisplayedText and [Component(obj, asString(realActiveDescendantDisplayedText))])       or (imageDescription and [Region(" "), Component(obj, asString(imageDescription))]))    + (realActiveDescendantRoleName and [Component(obj, (realActiveDescendantDisplayedText and " " or "") + asString(realActiveDescendantRoleName))])    + (expandableState and [Region(" " + asString(expandableState))])    + (required and [Region(" " + asString(required))]))or ([Component(obj,"")])'
                   }, 
                   pyatspi.ROLE_TEAROFF_MENU_ITEM: { 
                       'unfocused': '[Component(obj,           asString(roleName))]'
                   }, 
        pyatspi.ROLE_TERMINAL: { 
            'unfocused': '[Text(obj)]' }, 
        pyatspi.ROLE_TEXT: { 
            'unfocused': BRAILLE_TEXT }, 
        pyatspi.ROLE_TOGGLE_BUTTON: {
            'unfocused': '[Component(obj,           asString(((label + displayedText) or description) + expandableState + roleName),           indicator=asString(toggleState))]'
        }, } }
