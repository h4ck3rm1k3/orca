PAUSE_STR = 'pause'
TUTORIAL_STR = 'tutorial'
TUTORIAL = '(tutorial and (pause + tutorial) or [])'
MNEMONIC = '(mnemonic and (pause + mnemonic + lineBreak) or [])'

STR_READONLY= 'readOnly'
STR_OLDANCESTORS = 'oldAncestors'
STR_NEWANCESTORS = 'newAncestors'
STR_LABEL = 'label'
STR_TEXT_ROLE = 'textRole'
STR_TEXTCONTENTWITHATTRIBUTES = 'textContentWithAttributes'
STR_ROLE_NAME = 'roleName'
STR_VALUE = 'value'
STR_UNRELATEDLABELS = 'unrelatedLabels'
STR_AVAILABILITY = 'availability'
STR_NEWROWHEADER = 'newRowHeader'
STR_NEWNODELEVEL = 'newNodeLevel'
STR_POSITIONINLIST = 'positionInList'
STR_ACCELERATOR = 'accelerator'
STR_ALLTEXTSELECTION = 'allTextSelection'
STR_ANCESTORS = 'ancestors'
STR_ANYTEXTSELECTION = 'anyTextSelection'
STR_ASPAGETABORSCROLLPANE = 'asPageTabOrScrollPane'
STR_AVAILABILITY = 'availability'
STR_BASICWHEREAMI = 'basicWhereAmI'
STR_BRAILLE = 'braille'
STR_CELLCHECKEDSTATE = 'cellCheckedState'
STR_CHECKBOX = 'checkbox'
STR_CHECKEDSTATE = 'checkedState'
STR_CHILDWIDGET = 'childWidget'
STR_DEFAULT = 'default'
STR_DESCRIPTION = 'description'
STR_DETAILEDWHEREAMI = 'detailedWhereAmI'
STR_DISPLAYEDTEXT = 'displayedText'
STR_EMBEDDED = 'embedded'
STR_EOL = 'eol'
STR_EXPANDABLESTATE = 'expandableState'
STR_EXPANSION = 'expansion'
STR_FOCUSED = 'focused'
STR_FOCUSEDITEM = 'focusedItem'
STR_GROUPINDEX = 'groupindex'
STR_ICONINDEX = 'iconindex'
STR_IMAGEDESCRIPTION = 'imageDescription'
STR_INSENSITIVE = 'insensitive'
STR_LABELANDNAME = 'labelAndName'
STR_LABEL = 'label'
STR_LABELORNAME = 'labelOrName'
STR_LINKINFO = 'linkInfo'
STR_MULTISELECT = 'multiselect'
STR_NAMEDCONTAININGPANEL = 'namedContainingPanel'
STR_NAME = 'name'
STR_NESTINGLEVEL = 'nestinglevel'
STR_NEWCOLUMNHEADER = 'newColumnHeader'
STR_NEWNODELEVEL = 'newNodeLevel'
STR_NEWRADIOBUTTONGROUP = 'newRadioButtonGroup'
STR_NEWROWHEADER = 'newRowHeader'
STR_NODELEVEL = 'nodelevel'
STR_NUMBEROFCHILDREN = 'numberOfChildren'
STR_PARENTROLENAME = 'parentRoleName'
STR_PERCENTAGE = 'percentage'
STR_POSITIONINLIST = 'positionInList'
STR_PREFIX = 'prefix'
STR_RADIOBUTTONGROUP = 'radioButtonGroup'
STR_RADIOBUTTON = 'radiobutton'
STR_RADIOSTATE = 'radioState'
STR_READONLY1 = 'readonly'
STR_REAL_ROLE_TABLE_CELL = 'REAL_ROLE_TABLE_CELL'
STR_REQUIRED = 'required'
STR_ROLENAME = 'roleName'
STR_SELECTEDITEMCOUNT = 'selectedItemCount'
STR_SELECTEDITEMS = 'selectedItems'
STR_SPEECH = 'speech'
STR_STRINGS = 'strings'
STR_SUFFIX = 'suffix'
STR_TABLECELL2CHILDLABEL = 'tableCell2ChildLabel'
STR_TABLECELL2CHILDTOGGLE = 'tableCell2ChildToggle'
STR_TABLECELLROW = 'tableCellRow'
STR_TERMINAL = 'terminal'
STR_TEXTCONTENTWITHATTRIBUTES = 'textContentWithAttributes'
STR_TEXTROLE = 'textRole'
STR_TOGGLEBUTTON = 'togglebutton'
STR_TOOLBAR = 'toolbar'
STR_UNFOCUSED = 'unfocused'
STR_UNRELATEDLABELS = 'unrelatedLabels'
STR_UNSELECTEDCELL = 'unselectedCell'
STR_VALUE = 'value'

BRAILLE_TEXT = '[Text(obj, asString(label + placeholderText), asString(eol))]\
                + (required and [Region(" " + asString(required))])\
                + (readOnly and [Region(" " + asString(readOnly))])'
def _add(*args):
    '''
    x + t
    '''
    return " + ".join(args)

def _or(*args):
    '''
    x or t
    '''
    return " or ".join(args)

def _grp(*args):
    '''
    grouping ()
    '''
    return (
        "(" +
        " ".join(args)
        +  ")")

def emit():
    g = globals()
    for n in  g:
        v = g[n]

        if isinstance(v,str):
            print (n,v)

def replace(t):
    g = globals()
    for n in  g:
        v = g[n]
        if isinstance(v,str):
            #print n,v
            t= t.replace("'%s'" % v,n)
            t= t.replace(v,n)
    return t

#emit()
