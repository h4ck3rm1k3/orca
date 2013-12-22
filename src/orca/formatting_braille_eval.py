
class Something():
        def __call__(self, *args, ** kwargs):
                print "call %s" % __name__
                print args
                print kwargs
                return self

        def __getitem__(self, x):
                return Something()

        def __init__(self):
                pass

        def __add__(self, other):
                if isinstance(other, self.__class__):
                        return self
                elif isinstance(other, str):
                        return self
                else:
                        raise TypeError("unsupported operand type(s) for +: '{}' and '{}'").format(self.__class__, type(other))



accelerator = Something()
alertAndDialogCount = Something()
applicationName = Something()
asPageTabOrScrollPane = Something()

def asString(x) :
        return  "STR %s" % x

availability = Something()
cellCheckedState = Something()
checkedState = Something()
childWidget = [Something()]
columnHeaderIfToggleAndNoText = Something()
comboBoxTextObj = Something()
Component = Something()
currentLineText = Something()
description = Something()
displayedText = Something()
eol = Something()
expandableState = Something()
focusedItem = Something()
imageDescription = Something()
label = Something()
labelAndName = Something()
labelOrName = Something()
Link = Something()
menuItemCheckedState = Something()
name = Something()
nestingLevel = Something()
obj = Something()
placeholderText = Something()
radioState = Something()
readOnly = Something()
realActiveDescendantDisplayedText = Something()
realActiveDescendantRoleName = Something()
Region = Something()
required = Something()
roleName = Something()
space = Something()
tableCell2ChildLabel = Something()
tableCell2ChildToggle = Something()
tableCellRow = Something()
Text = Something()
toggleState = Something()
value = Something()

# for x in '''accelerator
# alertAndDialogCount
# applicationName
# asPageTabOrScrollPane
# asString
# availability
# cellCheckedState
# checkedState
# childWidget
# columnHeaderIfToggleAndNoText
# comboBoxTextObj
# Component
# currentLineText
# description
# displayedText
# eol
# expandableState
# focusedItem
# imageDescription
# label
# labelAndName
# labelOrName
# Link
# menuItemCheckedState
# name
# nestingLevel
# obj
# placeholderText
# radioState
# readOnly
# realActiveDescendantDisplayedText
# realActiveDescendantRoleName
# Region
# required
# roleName
# space
# tableCell2ChildLabel
# tableCell2ChildToggle
# tableCellRow
# Text
# toggleState
# value'''.split():
#         print "%s = Something()" % x 

def action_3_unfocused ():
	return [Component(obj,asString(label + displayedText + roleName + (description and space(": ") + description)))]
def action_6_unfocused ():
	return [Component(obj,asString(((label + displayedText + imageDescription) or name) + roleName))]
def action_7_unfocused ():
	return [Component(obj,asString(label + displayedText + roleName),indicator=asString(checkedState))]
def action_8_unfocused ():
	return [Component(obj,asString(label + displayedText + roleName + availability) + asString(accelerator),indicator=asString(checkedState))]
def action_73_unfocused ():
	return [Text(obj, asString(label + placeholderText), asString(eol))]                + (required and [Region(" " + asString(required))])                + (readOnly and [Region(" " + asString(readOnly))])
def action_11_unfocused ():
	return ((comboBoxTextObj and [Text(comboBoxTextObj[0], asString(label), asString(eol))]) or [Component(obj, asString(label + displayedText), label and (len(asString(label)) + 1) or 0)])+ [Region(" " + asString(roleName))]
def action_78_unfocused ():
	return [Component(obj,asString(label + displayedText) or asString(applicationName))]
def action_79_unfocused ():
	return [Text(obj, asString(label + placeholderText), asString(eol))]                + (required and [Region(" " + asString(required))])                + (readOnly and [Region(" " + asString(readOnly))])
def action_83_unfocused ():
	return [Text(obj)] + [Region(" " + asString(roleName))]
def action_23_focused ():
	return [Component(obj,asString(((label + displayedText) or name) + value + roleName + alertAndDialogCount))]
def action_23_unfocused ():
	return [Component(obj,asString(((label + displayedText) or name) + value + roleName + alertAndDialogCount))]
def action_88_unfocused ():
	return [Link(obj, asString(currentLineText)or asString(displayedText)or asString(name))]
def action_26_unfocused ():
	return [Component(obj,asString(((label + displayedText + imageDescription) or name) + roleName))]
def action_27_focused ():
	return [Component(obj,asString(labelAndName + value + roleName + required))]
def action_27_unfocused ():
	return [Component(obj,asString(labelAndName + value + roleName + required))]
def action_29_unfocused ():
	return [Text(obj,      asString(label),      asString(eol))]
def action_31_unfocused ():
	return [Component(obj,asString(label + focusedItem + roleName),asString(label) and (len(asString(label)) + 1) or 0)]

def action_32_focused ():
	return [
                Component(
                        obj,
                        asString(
                                label + displayedText + expandableState + roleName + availability
                        ) 
                        + 
                        asString(accelerator)
                )
        ]     +         (
                nestingLevel and [
                        Region(
                                " " + 
                                asString(
                                        nestingLevel
                                )
                        )
                ]
        )+  (
                childWidget and (
                        [
                                Region(" ")
                        ] + childWidget
                )
        )

def action_32_focused2 ():
	return [Component(obj,asString(label + displayedText + expandableState + roleName + availability) + asString(accelerator))]+ (nestingLevel and [Region(" " + asString(nestingLevel))])+ (childWidget and ([Region(" ")] + childWidget))


def action_32_unfocused ():
	return [Component(obj,asString(label + displayedText + expandableState))]+ (nestingLevel and [Region(" " + asString(nestingLevel))])+ (childWidget and ([Region(" ")] + childWidget))
def action_33_focused ():
	return [Component(obj,asString(label + displayedText + roleName + availability) + asString(accelerator))]
def action_33_unfocused ():
	return [Component(obj,asString(label + displayedText + roleName))]
def action_35_unfocused ():
	return [Component(obj,asString(label + displayedText + expandableState + availability) + asString(accelerator),indicator=asString(menuItemCheckedState))]
def action_37_focused ():
	return [Component(obj,asString(label + displayedText + roleName + availability) + asString(accelerator))]
def action_37_unfocused ():
	return [Component(obj,asString(label + displayedText + roleName))]
def action_39_unfocused ():
	return [Component(obj,asString((label or displayedText) + roleName))]+ (childWidget and ([Region(" ")] + childWidget))
def action_40_unfocused ():
	return [Text(obj, asString(label + placeholderText), asString(eol))]                + (required and [Region(" " + asString(required))])                + (readOnly and [Region(" " + asString(readOnly))])
def action_43_unfocused ():
	return [Component(obj,asString(((label + displayedText) or description) + expandableState + roleName))]
def action_44_unfocused ():
	return [Component(obj,asString(((label + displayedText) or description) + roleName),indicator=asString(radioState))]
def action_45_focused ():
	return [Component(obj,asString(((label + displayedText) or description) + roleName + availability)+ asString(accelerator),indicator=asString(radioState))]
def action_45_unfocused ():
	return [Component(obj,asString((label + displayedText) or description)+ asString(accelerator),indicator=asString(radioState))]
def action_REAL_ROLE_TABLE_CELL_unfocused ():
	return (tableCell2ChildToggle + tableCell2ChildLabel)or (cellCheckedState    + (columnHeaderIfToggleAndNoText and [Region(" "), Component(obj, asString(columnHeaderIfToggleAndNoText))])    + ((realActiveDescendantDisplayedText and [Component(obj, asString(realActiveDescendantDisplayedText))])       or (imageDescription and [Region(" "), Component(obj, asString(imageDescription))]))+ (realActiveDescendantRoleName and [Component(obj, (realActiveDescendantDisplayedText and " " or "") + asString(realActiveDescendantRoleName))])+ (expandableState and [Region(" " + asString(expandableState))])+ (required and [Region(" " + asString(required))]))or ([Component(obj,"")])
def action_other_default ():
	return {'focused': '[Component(obj,asString(label + displayedText + value + roleName + required))]', 'unfocused': '[Component(obj,asString(label + displayedText + value + roleName + required))]'}
def action_other_prefix ():
	return {'focused': '(includeContext and (ancestors  + (rowHeader and [Region(" " + asString(rowHeader))])  + (columnHeader and [Region(" " + asString(columnHeader))])  + (radioButtonGroup and [Region(" " + asString(radioButtonGroup))])  + [Region(" ")]) or [])', 'unfocused': '(includeContext and (ancestors  + (rowHeader and [Region(" " + asString(rowHeader))])  + (columnHeader and [Region(" " + asString(columnHeader))])  + (radioButtonGroup and [Region(" " + asString(radioButtonGroup))])  + [Region(" ")]) or [])'}
def action_other_suffix ():
	return {'focused': '(nodeLevel and [Region(" " + asString(nodeLevel))])', 'unfocused': '(nodeLevel and [Region(" " + asString(nodeLevel))])'}
def action_49_unfocused ():
	return asPageTabOrScrollPane
def action_51_unfocused ():
	return [Component(obj,asString(labelOrName + value + roleName + required))]
def action_52_unfocused ():
	return [Text(obj, asString(label), asString(eol))]+ (required and [Region(" " + asString(required))] or [])+ (readOnly and [Region(" " + asString(readOnly))] or [])
def action_56_unfocused ():
	return tableCellRow
def action_59_unfocused ():
	return [Component(obj,asString(roleName))]
def action_60_unfocused ():
	return [Text(obj)]
def action_61_unfocused ():
	return [Text(obj, asString(label + placeholderText), asString(eol))]                + (required and [Region(" " + asString(required))])                + (readOnly and [Region(" " + asString(readOnly))])
def action_62_unfocused ():
	return [Component(obj,asString(((label + displayedText) or description) + expandableState + roleName),indicator=asString(toggleState))]


action_11_unfocused ()
action_23_focused ()
action_23_unfocused ()
action_26_unfocused ()
action_27_focused ()
action_27_unfocused ()
action_29_unfocused ()
action_31_unfocused ()
action_32_focused ()
action_32_unfocused ()
action_33_focused ()
action_33_unfocused ()
action_35_unfocused ()
action_37_focused ()
action_37_unfocused ()
action_39_unfocused ()
action_3_unfocused ()
action_40_unfocused ()
action_43_unfocused ()
action_44_unfocused ()
action_45_focused ()
action_45_unfocused ()
action_49_unfocused ()
action_51_unfocused ()
action_52_unfocused ()
action_56_unfocused ()
action_59_unfocused ()
action_60_unfocused ()
action_61_unfocused ()
action_62_unfocused ()
action_6_unfocused ()
action_73_unfocused ()
action_78_unfocused ()
action_79_unfocused ()
action_7_unfocused ()
action_83_unfocused ()
action_88_unfocused ()
action_8_unfocused ()
action_REAL_ROLE_TABLE_CELL_unfocused ()
action_other_default ()
action_other_prefix ()
action_other_suffix ()
