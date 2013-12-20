# Orca
#
# Copyright 2005-2009 Sun Microsystems Inc.
# Copyright 2010-2013 The Orca Team
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

"""Implements structural navigation."""

__id__ = "$Id$"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2005-2009 Sun Microsystems Inc." \
                "Copyright (c) 2010-2013 The Orca Team"
__license__ = "LGPL"

import pyatspi

from . import cmdnames
from . import debug
from . import guilabels
from . import input_event
from . import keybindings
from . import messages
from . import object_properties
from . import orca
from . import orca_gui_navlist
from . import orca_state
from . import settings
from . import speech

#
#
# MatchCriteria                                                             #
#
#

class MatchCriteria(object):

    """Contains the criteria which will be used to generate a collection
    matchRule.  We don't want to create the rule until we need it and
    are ready to use it. In addition, the creation of an AT-SPI match
    rule requires you specify quite a few things (see the __init__),
    most of which are irrelevant to the search at hand.  This class
    makes it possible for the StructuralNavigationObject creator to just
    specify the few criteria that actually matter.
    """

    def __init__(self,
                 collection,
                 states=[],
                 matchStates=None,
                 objAttrs=[],
                 matchObjAttrs=None,
                 roles=[],
                 matchRoles=None,
                 interfaces="",
                 matchInterfaces=None,
                 invert=False,
                 applyPredicate=False):
        """Creates a new match criteria object.

        Arguments:
        - collection: the collection interface for the document in
          which the accessible objects can be found.
        - states: a list of pyatspi states of interest
        - matchStates: whether an object must have all of the states
          in the states list, any of the states in the list, or none
          of the states in the list.  Must be one of the collection
          interface MatchTypes if provided.
        - objAttrs: a list of object attributes (not text attributes)
        - matchObjAttrs: whether an object must have all of the
          attributes in the objAttrs list, any of the attributes in
          the list, or none of the attributes in the list.  Must be
          one of the collection interface MatchTypes if provided.
        - interfaces: (We aren't using this.  According to the at-spi
          idl, it is a string.)
        - matchInterfaces: The collection MatchType for matching by
          interface.
        - invert: If true the match rule will find objects that don't
          match. We always use False.
        - applyPredicate: whether or not a predicate should be applied
          as an additional check to see if an item is indeed a match.
          This is necessary, for instance, when one of the things we
          care about is a text attribute, something the collection
          interface doesn't include in its criteria.
        """

        self.collection = collection
        self.matchStates = matchStates or collection.MATCH_ANY
        self.objAttrs = objAttrs
        self.matchObjAttrs = matchObjAttrs or collection.MATCH_ANY
        self.roles = roles
        self.matchRoles = matchRoles or collection.MATCH_ANY
        self.interfaces = interfaces
        self.matchInterfaces = matchInterfaces or collection.MATCH_ALL
        self.invert = invert
        self.applyPredicate = applyPredicate

        self.states = pyatspi.StateSet()
        for state in states:
            self.states.add(state)

#
#
# StructuralNavigationObject                                              #
#
#

class StructuralNavigationObject(object):

    """Represents a document object which has identifiable characteristics
    which can be used for the purpose of navigation to and among instances
    of that object. These characteristics may be something as simple as a
    role and/or a state of interest. Or they may be something more complex
    such as character counts, text attributes, and other object attributes.
    """

    def __init__(self, structuralNavigation, objType, bindings, predicate,
                 criteria, presentation, dialogData):
        """Creates a new structural navigation object.

        Arguments:
        - structuralNavigation: the StructuralNavigation class associated
          with this object.
        - objType: the type (e.g. BLOCKQUOTE) associated with this object.
        - bindings: a dictionary of all of the possible bindings for this
          object.  In the case of all but the "atLevel" bindings, each
          binding takes the form of [keysymstring, modifiers, description].
          The goPreviousAtLevel and goNextAtLevel bindings are each a list
          of bindings in that form.
        - predicate: the predicate to use to determine if a given accessible
          matches this structural navigation object. Used when a search via
          collection is not possible or practical.
        - criteria: a method which returns a MatchCriteria object which
          can in turn be used to locate the next/previous matching accessible
          via collection.
        - presentation: the method which should be called after performing
          the search for the structural navigation object.
        - dialogData: the method which returns the title, column headers,
          and row data which should be included in the "list of" dialog for
          the structural navigation object.
        """

        self.structuralNavigation = structuralNavigation
        self.objType = objType
        self.bindings = bindings
        self.predicate = predicate
        self.criteria = criteria
        self.present = presentation
        self._dialogData = dialogData

        self.inputEventHandlers = {}
        self.keyBindings = keybindings.KeyBindings()
        self.functions = []
        self._setUpHandlersAndBindings()

    def _setUpHandlersAndBindings(self):
        """Adds the inputEventHandlers and keyBindings for this object."""

        # Set up the basic handlers.  These are our traditional goPrevious
        # and goNext functions.
        #
        previousBinding = self.bindings.get("previous")
        if previousBinding:
            [keysymstring, modifiers, description] = previousBinding
            handlerName = "%sGoPrevious" % self.objType
            self.inputEventHandlers[handlerName] = \
                input_event.InputEventHandler(self.goPrevious, description)

            self.keyBindings.add(
                keybindings.KeyBinding(
                    keysymstring,
                    settings.defaultModifierMask,
                    modifiers,
                    self.inputEventHandlers[handlerName]))

            self.functions.append(self.goPrevious)

        nextBinding = self.bindings.get("next")
        if nextBinding:
            [keysymstring, modifiers, description] = nextBinding
            handlerName = "%sGoNext" % self.objType
            self.inputEventHandlers[handlerName] = \
                input_event.InputEventHandler(self.goNext, description)

            self.keyBindings.add(
                keybindings.KeyBinding(
                    keysymstring,
                    settings.defaultModifierMask,
                    modifiers,
                    self.inputEventHandlers[handlerName]))

            self.functions.append(self.goNext)

        listBinding = self.bindings.get("list")
        if listBinding:
            [keysymstring, modifiers, description] = listBinding
            handlerName = "%sShowList" % self.objType
            self.inputEventHandlers[handlerName] = \
                input_event.InputEventHandler(self.showList, description)

            self.keyBindings.add(
                keybindings.KeyBinding(
                    keysymstring,
                    settings.defaultModifierMask,
                    modifiers,
                    self.inputEventHandlers[handlerName]))

        # Set up the "at level" handlers (e.g. to navigate among headings
        # at the specified level).
        #
        previousAtLevel = self.bindings.get("previousAtLevel") or []
        for i, binding in enumerate(previousAtLevel):
            level = i + 1
            handler = self.goPreviousAtLevelFactory(level)
            handlerName = "%sGoPreviousLevel%dHandler" % (self.objType, level)
            keysymstring, modifiers, description = binding

            self.inputEventHandlers[handlerName] = \
                input_event.InputEventHandler(handler, description)

            self.keyBindings.add(
                keybindings.KeyBinding(
                    keysymstring,
                    settings.defaultModifierMask,
                    modifiers,
                    self.inputEventHandlers[handlerName]))

            self.functions.append(handler)

        nextAtLevel = self.bindings.get("nextAtLevel") or []
        for i, binding in enumerate(nextAtLevel):
            level = i + 1
            handler = self.goNextAtLevelFactory(level)
            handlerName = "%sGoNextLevel%dHandler" % (self.objType, level)
            keysymstring, modifiers, description = binding

            self.inputEventHandlers[handlerName] = \
                input_event.InputEventHandler(handler, description)

            self.keyBindings.add(
                keybindings.KeyBinding(
                    keysymstring,
                    settings.defaultModifierMask,
                    modifiers,
                    self.inputEventHandlers[handlerName]))

            self.functions.append(handler)

        listAtLevel = self.bindings.get("listAtLevel") or []
        for i, binding in enumerate(listAtLevel):
            level = i + 1
            handler = self.showListAtLevelFactory(level)
            handlerName = "%sShowListAtLevel%dHandler" % (self.objType, level)
            keysymstring, modifiers, description = binding

            self.inputEventHandlers[handlerName] = \
                input_event.InputEventHandler(handler, description)

            self.keyBindings.add(
                keybindings.KeyBinding(
                    keysymstring,
                    settings.defaultModifierMask,
                    modifiers,
                    self.inputEventHandlers[handlerName]))

        # Set up the "directional" handlers (e.g. for table cells. Live
        # region support has a handler to go to the last live region,
        # so we'll handle that here as well).
        #
        directions = {}
        directions["Left"] = self.bindings.get("left")
        directions["Right"] = self.bindings.get("right")
        directions["Up"] = self.bindings.get("up")
        directions["Down"] = self.bindings.get("down")
        directions["First"] = self.bindings.get("first")
        directions["Last"] = self.bindings.get("last")

        for direction in directions:
            binding = directions.get(direction)
            if not binding:
                continue

            handler = self.goDirectionFactory(direction)
            handlerName = "%sGo%s" % (self.objType, direction)
            keysymstring, modifiers, description = binding

            self.inputEventHandlers[handlerName] = \
                input_event.InputEventHandler(handler, description)

            self.keyBindings.add(
                keybindings.KeyBinding(
                    keysymstring,
                    settings.defaultModifierMask,
                    modifiers,
                    self.inputEventHandlers[handlerName]))

            self.functions.append(handler)

    def addHandlerAndBinding(self, binding, handlerName, function):
        """Adds a custom inputEventHandler and keybinding to the object's
        handlers and bindings.  Right now this is unused, but here in
        case a creator of a StructuralNavigationObject had some other
        desired functionality in mind.

        Arguments:
        - binding: [keysymstring, modifiers, description]
        - handlerName: a string uniquely identifying the handler
        - function: the function associated with the binding
        """

        [keysymstring, modifiers, description] = binding
        handler = input_event.InputEventHandler(function, description)
        keyBinding = keybindings.KeyBinding(
            keysymstring,
            settings.defaultModifierMask,
            modifiers,
            handler)

        self.inputEventHandlers[handlerName] = handler
        self.structuralNavigation.inputEventHandlers[handlerName] = handler

        self.functions.append(function)
        self.structuralNavigation.functions.append(function)

        self.keyBindings.add(keyBinding)
        self.structuralNavigation.keyBindings.add(keyBinding)

    def goPrevious(self, script, inputEvent):
        """Go to the previous object."""
        self.structuralNavigation.goObject(self, False)

    def goNext(self, script, inputEvent):
        """Go to the next object."""
        self.structuralNavigation.goObject(self, True)

    def showList(self, script, inputEvent):
        """Show a list of all the items with this object type."""

        try:
            objects = self.structuralNavigation._getAll(self)
        except:
            script.presentMessage(messages.NAVIGATION_DIALOG_ERROR)
            return

        title, columnHeaders, rowData = self._dialogData()
        count = len(objects)
        title = "%s: %s" % (title, messages.itemsFound(count))
        if not count:
            script.presentMessage(title)
            return

        currentObject = self.structuralNavigation.getCurrentObject()
        try:
            index = objects.index(currentObject)
        except:
            index = 0

        rows = [[obj] + rowData(obj) for obj in objects]
        orca_gui_navlist.showUI(title, columnHeaders, rows, index)

    def goPreviousAtLevelFactory(self, level):
        """Generates a goPrevious method for the specified level. Right
        now, this is just for headings, but it may have applicability
        for other objects such as list items (i.e. for level-based
        navigation in an outline or other multi-tiered list.

        Arguments:
        - level: the desired level of the object as an int.
        """

        def goPreviousAtLevel(script, inputEvent):
            self.structuralNavigation.goObject(self, False, arg=level)
        return goPreviousAtLevel

    def goNextAtLevelFactory(self, level):
        """Generates a goNext method for the specified level. Right
        now, this is just for headings, but it may have applicability
        for other objects such as list items (i.e. for level-based
        navigation in an outline or other multi-tiered list.

        Arguments:
        - level: the desired level of the object as an int.

        """

        def goNextAtLevel(script, inputEvent):
            self.structuralNavigation.goObject(self, True, arg=level)
        return goNextAtLevel

    def showListAtLevelFactory(self, level):
        """Generates a showList method for the specified level. Right
        now, this is just for headings, but it may have applicability
        for other objects such as list items (i.e. for level-based
        navigation in an outline or other multi-tiered list.

        Arguments:
        - level: the desired level of the object as an int.
        """

        def showListAtLevel(script, inputEvent):
            try:
                objects = self.structuralNavigation._getAll(self, arg=level)
            except:
                script.presentMessage(messages.NAVIGATION_DIALOG_ERROR)
                return

            title, columnHeaders, rowData = self._dialogData(arg=level)
            count = len(objects)
            title = "%s: %s" % (title, messages.itemsFound(count))
            if not count:
                script.presentMessage(title)
                return

            currentObject = self.structuralNavigation.getCurrentObject()
            try:
                index = objects.index(currentObject)
            except:
                index = 0

            rows = [[obj] + rowData(obj) for obj in objects]
            orca_gui_navlist.showUI(title, columnHeaders, rows, index)

        return showListAtLevel

    def goDirectionFactory(self, direction):
        """Generates the methods for navigation in a particular direction
        (i.e. left, right, up, down, first, last).  Right now, this is
        primarily for table cells, but it may have applicability for other
        objects.  For example, when navigating in an outline, one might
        want the ability to navigate to the next item at a given level,
        but then work his/her way up/down in the hierarchy.

        Arguments:
        - direction: the direction in which to navigate as a string.
        """

        def goCell(script, inputEvent):
            thisCell = self.structuralNavigation.getCellForObj(
                self.structuralNavigation.getCurrentObject())
            currentCoordinates = \
                self.structuralNavigation.getCellCoordinates(thisCell)
            if direction == "Left":
                desiredCoordinates = [currentCoordinates[0],
                                      currentCoordinates[1] - 1]
            elif direction == "Right":
                desiredCoordinates = [currentCoordinates[0],
                                      currentCoordinates[1] + 1]
            elif direction == "Up":
                desiredCoordinates = [currentCoordinates[0] - 1,
                                      currentCoordinates[1]]
            elif direction == "Down":
                desiredCoordinates = [currentCoordinates[0] + 1,
                                      currentCoordinates[1]]
            elif direction == "First":
                desiredCoordinates = [0, 0]
            else:
                desiredCoordinates = [-1, -1]
                table = self.structuralNavigation.getTableForCell(thisCell)
                if table:
                    iTable = table.queryTable()
                    lastRow = iTable.nRows - 1
                    lastCol = iTable.nColumns - 1
                    desiredCoordinates = [lastRow, lastCol]
            self.structuralNavigation.goCell(self,
                                             thisCell,
                                             currentCoordinates,
                                             desiredCoordinates)

        def goLastLiveRegion(script, inputEvent):
            """Go to the last liveRegion."""
            if settings.inferLiveRegions:
                script.liveMngr.goLastLiveRegion()
            else:
                script.presentMessage(messages.LIVE_REGIONS_OFF)

        if self.objType == StructuralNavigation.TABLE_CELL:
            return goCell
        elif self.objType == StructuralNavigation.LIVE_REGION \
                and direction == "Last":
            return goLastLiveRegion

#
#
# StructuralNavigation                                                      #
#
#

class StructuralNavigation(object):

    """This class implements the structural navigation functionality which
    is available to scripts. Scripts interested in implementing structural
    navigation need to override getEnabledStructuralNavigationTypes() and
    return a list of StructuralNavigation object types which should be
    enabled.
    """

    # The available object types.
    #
    # Convenience methods have been put into place whereby one can
    # create an object (FOO = "foo"), and then provide the following
    # methods: _fooBindings(), _fooPredicate(), _fooCriteria(), and
    # _fooPresentation(). With these in place, and with the object
    # FOO included among the object types returned by the script's
    # getEnabledStructuralNavigationTypes(), the StructuralNavigation
    # object should be created and set up automagically. At least that
    # is the idea. :-) This hopefully will also enable easy re-definition
    # of existing StructuralNavigationObjects on a script-by-script basis.
    # For instance, in the soffice script, overriding _blockquotePredicate
    # should be all that is needed to implement navigation by blockquote
    # in OOo Writer documents.
    #
    ANCHOR = "anchor"
    BLOCKQUOTE = "blockquote"
    BUTTON = "button"
    CHECK_BOX = "checkBox"
    CHUNK = "chunk"
    COMBO_BOX = "comboBox"
    ENTRY = "entry"
    FORM_FIELD = "formField"
    HEADING = "heading"
    LANDMARK = "landmark"
    LINK = "link"
    LIST = "list"        # Bulleted/numbered lists
    LIST_ITEM = "listItem"    # Bulleted/numbered list items
    LIVE_REGION = "liveRegion"
    PARAGRAPH = "paragraph"
    RADIO_BUTTON = "radioButton"
    SEPARATOR = "separator"
    TABLE = "table"
    TABLE_CELL = "tableCell"
    UNVISITED_LINK = "unvisitedLink"
    VISITED_LINK = "visitedLink"

    # Roles which are recognized as being a form field. Note that this
    # is for the purpose of match rules and predicates and refers to
    # AT-SPI roles.
    #
    FORM_ROLES = [pyatspi.ROLE_CHECK_BOX,
                  pyatspi.ROLE_RADIO_BUTTON,
                  pyatspi.ROLE_COMBO_BOX,
                  pyatspi.ROLE_DOCUMENT_FRAME, # rich text editing
                  pyatspi.ROLE_LIST,
                  pyatspi.ROLE_ENTRY,
                  pyatspi.ROLE_PASSWORD_TEXT,
                  pyatspi.ROLE_PUSH_BUTTON,
                  pyatspi.ROLE_SPIN_BUTTON,
                  pyatspi.ROLE_TEXT]

    # Roles which are recognized as being potential "large objects"
    # or "chunks." Note that this refers to AT-SPI roles.
    #
    OBJECT_ROLES = [pyatspi.ROLE_HEADING,
                    pyatspi.ROLE_LIST,
                    pyatspi.ROLE_PARAGRAPH,
                    pyatspi.ROLE_TABLE,
                    pyatspi.ROLE_TABLE_CELL,
                    pyatspi.ROLE_TEXT,
                    pyatspi.ROLE_SECTION,
                    pyatspi.ROLE_DOCUMENT_FRAME]

    def __init__(self, script, enabledTypes, enabled=False):
        """Creates an instance of the StructuralNavigation class.

        Arguments:
        - script: the script which which this instance is associated.
        - enabledTypes: a list of StructuralNavigation object types
          which the script is interested in supporting.
        - enabled: Whether structural navigation should start out
          enabled.  For instance, in Gecko by default we do what it
          enabled; in soffice, we would want to start out with it
          disabled and have the user enable it via a keystroke when
          desired.
        """

        self._script = script
        self.enabled = enabled

        # Create all of the StructuralNavigationObject's in which the
        # script is interested, using the convenience method
        #
        self.enabledObjects = {}
        for objType in enabledTypes:
            self.enabledObjects[objType] = \
                self.structuralNavigationObjectCreator(objType)

        self.functions = []
        self.inputEventHandlers = {}
        self.setupInputEventHandlers()
        self.keyBindings = self.getKeyBindings()

        # When navigating in a non-uniform table, one can move to a
        # cell which spans multiple rows and/or columns.  When moving
        # beyond that cell, into a cell that does NOT span multiple
        # rows/columns, we want to be sure we land in the right place.
        # Therefore, we'll store the coordinates from "our perspective."
        #
        self.lastTableCell = [-1, -1]

    def structuralNavigationObjectCreator(self, name):
        """This convenience method creates a StructuralNavigationObject
        with the specified name and associated characterists. (See the
        "Objects" section of code near the end of this class. Creators
        of StructuralNavigationObject's can still do things the old
        fashioned way should they so choose, by creating the instance
        and then adding it via addObject().

        Arguments:
        - name: the name/objType associated with this object.
        """

        # We're going to assume bindings.  After all, a structural
        # navigation object is by defintion an object which one can
        # navigate to using the associated keybindings. For similar
        # reasons we'll also assume a predicate and a presentation
        # method.  (See the Objects section towards the end of this
        # class for examples of each.)
        #
        bindings = eval("self._%sBindings()" % name)
        criteria = eval("self._%sCriteria" % name)
        predicate = eval("self._%sPredicate" % name)
        presentation = eval("self._%sPresentation" % name)

        try:
            dialogData = eval("self._%sDialogData" % name)
        except:
            dialogData = None

        return StructuralNavigationObject(self, name, bindings, predicate,
                                          criteria, presentation, dialogData)

    def addObject(self, objType, structuralNavigationObject):
        """Adds structuralNavigationObject to the dictionary of enabled
        objects.

        Arguments:
        - objType: the name/object type of the StructuralNavigationObject.
        - structuralNavigationObject: the StructuralNavigationObject to
          add.
        """

        self.enabledObjects[objType] = structuralNavigationObject

    def setupInputEventHandlers(self):
        """Defines InputEventHandler fields for a script."""

        if not len(self.enabledObjects):
            return

        self.inputEventHandlers["toggleStructuralNavigationHandler"] = \
            input_event.InputEventHandler(
                self.toggleStructuralNavigation,
                cmdnames.STRUCTURAL_NAVIGATION_TOGGLE)

        for structuralNavigationObject in list(self.enabledObjects.values()):
            self.inputEventHandlers.update(
                structuralNavigationObject.inputEventHandlers)
            self.functions.extend(structuralNavigationObject.functions)

    def getKeyBindings(self):
        """Defines the structural navigation key bindings for a script.

        Returns: an instance of keybindings.KeyBindings.
        """

        keyBindings = keybindings.KeyBindings()

        if not len(self.enabledObjects):
            return keyBindings

        keyBindings.add(
            keybindings.KeyBinding(
                "z",
                settings.defaultModifierMask,
                settings.ORCA_MODIFIER_MASK,
                self.inputEventHandlers["toggleStructuralNavigationHandler"]))

        for structuralNavigationObject in list(self.enabledObjects.values()):
            bindings = structuralNavigationObject.keyBindings.keyBindings
            for keybinding in bindings:
                keyBindings.add(keybinding)

        return keyBindings
    #
    #
    # Input Event Handler Methods                                           #
    #
    #

    def toggleStructuralNavigation(self, script, inputEvent):
        """Toggles structural navigation keys."""

        self.enabled = not self.enabled

        if self.enabled:
            string = messages.STRUCTURAL_NAVIGATION_KEYS_ON
        else:
            string = messages.STRUCTURAL_NAVIGATION_KEYS_OFF

        debug.println(debug.LEVEL_CONFIGURATION, string)
        self._script.presentMessage(string)
    #
    #
    # Methods for Moving to Objects                                         #
    #
    #

    def goCell(self, structuralNavigationObject, thisCell,
               currentCoordinates, desiredCoordinates):
        """The method used for navigation among cells in a table.

        Arguments:
        - structuralNavigationObject: the StructuralNavigationObject which
          represents the table cell.
        - thisCell: the pyatspi accessible TABLE_CELL we're currently in
        - currentCoordinates: the [row, column] of thisCell.  Note, we
          cannot just get the coordinates because in table cells which
          span multiple rows and/or columns, the value returned by
          table.getRowAtIndex() is the first row the cell spans. Likewise,
          the value returned by table.getColumnAtIndex() is the left-most
          column.  Therefore, we keep track of the row and column from
          our perspective to ensure we stay in the correct row and column.
        - desiredCoordinates: the [row, column] where we think we'd like to
          be.
        """

        table = self.getTableForCell(thisCell)
        try:
            iTable = table.queryTable()
        except:
            self._script.presentMessage(messages.TABLE_NOT_IN_A)
            return None

        currentRow, currentCol = currentCoordinates
        desiredRow, desiredCol = desiredCoordinates
        rowDiff = desiredRow - currentRow
        colDiff = desiredCol - currentCol
        oldRowHeaders = self._getRowHeaders(thisCell)
        oldColHeaders = self._getColumnHeaders(thisCell)
        cell = thisCell
        while cell:
            cell = iTable.getAccessibleAt(desiredRow, desiredCol)
            if not cell:
                if desiredCol < 0:
                    self._script.presentMessage(messages.TABLE_ROW_BEGINNING)
                    desiredCol = 0
                elif desiredCol > iTable.nColumns - 1:
                    self._script.presentMessage(messages.TABLE_ROW_END)
                    desiredCol = iTable.nColumns - 1
                if desiredRow < 0:
                    self._script.presentMessage(messages.TABLE_COLUMN_TOP)
                    desiredRow = 0
                elif desiredRow > iTable.nRows - 1:
                    self._script.presentMessage(messages.TABLE_COLUMN_BOTTOM)
                    desiredRow = iTable.nRows - 1
            elif self._script.utilities.isSameObject(thisCell, cell) \
                    or settings.skipBlankCells and self._isBlankCell(cell):
                if colDiff < 0:
                    desiredCol -= 1
                elif colDiff > 0:
                    desiredCol += 1
                if rowDiff < 0:
                    desiredRow -= 1
                elif rowDiff > 0:
                    desiredRow += 1
            else:
                break

        self.lastTableCell = [desiredRow, desiredCol]
        if cell:
            arg = [rowDiff, colDiff, oldRowHeaders, oldColHeaders]
            structuralNavigationObject.present(cell, arg)

    def _getAll(self, structuralNavigationObject, arg=None):
        """Returns all the instances of structuralNavigationObject."""
        if not structuralNavigationObject.criteria:
            return []

        document = self._getDocument()
        col = document.queryCollection()
        criteria = structuralNavigationObject.criteria(col, arg)
        rule = col.createMatchRule(criteria.states.raw(),
                                   criteria.matchStates,
                                   criteria.objAttrs,
                                   criteria.matchObjAttrs,
                                   criteria.roles,
                                   criteria.matchRoles,
                                   criteria.interfaces,
                                   criteria.matchInterfaces,
                                   criteria.invert)
        rv = col.getMatches(rule, col.SORT_ORDER_CANONICAL, 0, True)
        col.freeMatchRule(rule)
        if criteria.applyPredicate:
            rv = list(filter(structuralNavigationObject.predicate, rv))

        return rv

    def goObject(self, structuralNavigationObject, isNext, obj=None, arg=None):
        """The method used for navigation among StructuralNavigationObjects
        which are not table cells.

        Arguments:
        - structuralNavigationObject: the StructuralNavigationObject which
          represents the object of interest.
        - isNext: If True, we're interested in the next accessible object
          which matches structuralNavigationObject.  If False, we're
          interested in the previous accessible object which matches.
        - obj: the current object (typically the locusOfFocus).
        - arg: optional arguments which may need to be passed along to
          the predicate, presentation method, etc. For instance, in the
          case of navigating amongst headings at a given level, the level
          is needed and passed in as arg.
        """

        obj = obj or self.getCurrentObject()

        try:
            state = obj.getState()
        except:
            return [None, False]
        else:
            if state.contains(pyatspi.STATE_DEFUNCT):
                debug.printException(debug.LEVEL_SEVERE)
                return [None, False]

        wrap = settings.wrappedStructuralNavigation
        document = self._getDocument()
        if not document:
            return

        collection = document.queryCollection()
        criteria = structuralNavigationObject.criteria(collection, arg)

        # If the document frame itself contains content and that is
        # our current object, querying the collection interface will
        # result in our starting at the top when looking for the next
        # object rather than the current caret offset. See bug 567984.
        #
        if isNext and self._script.utilities.isSameObject(obj, document):
            pred = self.isAfterDocumentOffset
            if criteria.applyPredicate:
                pred = pred and structuralNavigationObject.predicate
            criteria.applyPredicate = True
            structuralNavigationObject.predicate = pred

        rule = collection.createMatchRule(criteria.states.raw(),
                                          criteria.matchStates,
                                          criteria.objAttrs,
                                          criteria.matchObjAttrs,
                                          criteria.roles,
                                          criteria.matchRoles,
                                          criteria.interfaces,
                                          criteria.matchInterfaces,
                                          criteria.invert)
        if criteria.applyPredicate:
            predicate = structuralNavigationObject.predicate
        else:
            predicate = None

        if not isNext:
            [obj, wrapped] = self._findPrevByMatchRule(collection,
                                                       rule,
                                                       wrap,
                                                       obj,
                                                       predicate)
        else:
            [obj, wrapped] = self._findNextByMatchRule(collection,
                                                       rule,
                                                       wrap,
                                                       obj,
                                                       predicate)
            collection.freeMatchRule(rule)

        if wrapped:
            if not isNext:
                self._script.presentMessage(messages.WRAPPING_TO_BOTTOM)
            else:
                self._script.presentMessage(messages.WRAPPING_TO_TOP)

        structuralNavigationObject.present(obj, arg)
    #
    #
    # Utility Methods for Finding Objects                                   #
    #
    #

    def getCurrentObject(self):
        """Returns the current object.  Normally, the locusOfFocus. But
        in the case of Gecko, that doesn't always work.
        """

        return orca_state.locusOfFocus

    def isAfterDocumentOffset(self, obj, arg=None):
        """Returns True if obj is after the document's caret offset."""
        document = self._getDocument()
        try:
            offset = document.queryText().caretOffset
        except:
            return False

        start, end = self._script.utilities.getHyperlinkRange(obj)
        if start > offset:
            return True

        try:
            hypertext = document.queryHypertext()
            hyperlink = hypertext.getLink(hypertext.getNLinks() - 1)
        except:
            return False

        return offset > hyperlink.startIndex

    def _findPrevByMatchRule(self, collection, matchRule, wrap, currentObj,
                             predicate=None):
        """Finds the previous object using the given match rule as a
        pattern to match or not match.

        Arguments:
        -collection: the accessible collection interface
        -matchRule: the collections match rule to use
        -wrap: if True and the bottom of the document is reached, move
         to the top and keep looking.
        -currentObj: the object from which the search should begin
        -predicate: an optional predicate to further test if the item
         found via collection is indeed a match.

        Returns: [obj, wrapped] where wrapped is a boolean reflecting
        whether wrapping took place.
        """

        currentObj = currentObj or self.getCurrentObject()
        document = self._getDocument()

        # If the current object is the document itself, find an actual
        # object to use as the starting point. Otherwise we're in
        # danger of skipping over the objects in between our present
        # location and top of the document.
        #
        if self._script.utilities.isSameObject(currentObj, document):
            currentObj = self._findNextObject(currentObj, document)

        ancestors = []
        obj = currentObj.parent
        if obj.getRole() in [pyatspi.ROLE_LIST, pyatspi.ROLE_TABLE]:
            ancestors.append(obj)
        else:
            while obj:
                ancestors.append(obj)
                obj = obj.parent

        match, wrapped = None, False
        results = collection.getMatchesTo(currentObj,
                                          matchRule,
                                          collection.SORT_ORDER_CANONICAL,
                                          collection.TREE_INORDER,
                                          True,
                                          1,
                                          True)
        while not match:
            if len(results) == 0:
                if wrapped or not wrap:
                    break
                elif wrap:
                    lastObj = self._findLastObject(document)
                    if self._script.utilities.isSameObject(lastObj, document):
                        wrapped = True
                        continue

                    # Collection does not do an inclusive search, meaning
                    # that the start object is not part of the search.  So
                    # we need to test the lastobj separately using the given
                    # matchRule.  We don't have this problem for 'Next' because
                    # the startobj is the doc frame.
                    #
                    secondLastObj = self._findPreviousObject(lastObj, document)
                    results = collection.getMatchesFrom(
                        secondLastObj,
                        matchRule,
                        collection.SORT_ORDER_CANONICAL,
                        collection.TREE_INORDER,
                        1,
                        True)
                    wrapped = True
                    if len(results) > 0 \
                       and (not predicate or predicate(results[0])):
                        match = results[0]
                    else:
                        results = collection.getMatchesTo(
                            lastObj,
                            matchRule,
                            collection.SORT_ORDER_CANONICAL,
                            collection.TREE_INORDER,
                            True,
                            1,
                            True)
            elif len(results) > 0:
                if results[0] in ancestors \
                   or predicate and not predicate(results[0]):
                    results = collection.getMatchesTo(
                        results[0],
                        matchRule,
                        collection.SORT_ORDER_CANONICAL,
                        collection.TREE_INORDER,
                        True,
                        1,
                        True)
                else:
                    match = results[0]

        return [match, wrapped]

    def _findNextByMatchRule(self, collection, matchRule, wrap, currentObj,
                             predicate=None):
        """Finds the next object using the given match rule as a pattern
        to match or not match.

        Arguments:
        -collection:  the accessible collection interface
        -matchRule: the collections match rule to use
        -wrap: if True and the bottom of the document is reached, move
         to the top and keep looking.
        -currentObj: the object from which the search should begin
        -predicate: an optional predicate to further test if the item
         found via collection is indeed a match.

        Returns: [obj, wrapped] where wrapped is a boolean reflecting
        whether wrapping took place.
        """

        currentObj = currentObj or self.getCurrentObject()
        ancestors = []
        [currentObj, offset] = self._script.getCaretContext()
        obj = currentObj.parent
        while obj:
            ancestors.append(obj)
            obj = obj.parent

        match, wrapped = None, False
        while not match:
            results = collection.getMatchesFrom(
                currentObj,
                matchRule,
                collection.SORT_ORDER_CANONICAL,
                collection.TREE_INORDER,
                1,
                True)
            if len(results) > 0 and not results[0] in ancestors:
                currentObj = results[0]
                if not predicate or predicate(currentObj):
                    match = currentObj
            elif wrap and not wrapped:
                wrapped = True
                ancestors = [currentObj]
                currentObj = self._getDocument()
            else:
                break

        return [match, wrapped]

    def _findPreviousObject(self, obj, stopAncestor):
        """Finds the object prior to this one, where the tree we're
        dealing with is a DOM and 'prior' means the previous object
        in a linear presentation sense.

        Arguments:
        -obj: the object where to start.
        -stopAncestor: the ancestor at which the search should stop
        """

        # NOTE: This method is based on some intial experimentation
        # with OOo structural navigation.  It might need refining
        # or fixing and is being overridden by the Gecko method
        # regardless, so this one can be modified as appropriate.
        #
        prevObj = None

        index = obj.getIndexInParent() - 1
        if index >= 0:
            prevObj = obj.parent[index]
            if not prevObj:
                debug.println(debug.LEVEL_FINE, 'Error: Dead Accessible')
            elif prevObj.childCount:
                prevObj = prevObj[prevObj.childCount - 1]
        elif not self._script.utilities.isSameObject(obj.parent, stopAncestor):
            prevObj = obj.parent

        return prevObj

    def _findNextObject(self, obj, stopAncestor):
        """Finds the object after to this one, where the tree we're
        dealing with is a DOM and 'next' means the next object
        in a linear presentation sense.

        Arguments:
        -obj: the object where to start.
        -stopAncestor: the ancestor at which the search should stop
        """

        # NOTE: This method is based on some intial experimentation
        # with OOo structural navigation.  It might need refining
        # or fixing and is being overridden by the Gecko method
        # regardless, so this one can be modified as appropriate.
        #
        nextObj = None

        if obj and obj.childCount:
            nextObj = obj[0]

        while obj and obj.parent != obj and not nextObj:
            index = obj.getIndexInParent() + 1
            if 0 < index < obj.parent.childCount:
                nextObj = obj.parent[index]
                if not nextObj:
                    debug.println(debug.LEVEL_FINE, 'Error: Dead Accessible')
                    break
            elif not self._script.utilities.isSameObject(
                    obj.parent, stopAncestor):
                obj = obj.parent
            else:
                break

        return nextObj

    def _findLastObject(self, ancestor):
        """Returns the last object in ancestor.

        Arguments:
        - ancestor: the accessible object whose last (child) object
          is sought.
        """

        # NOTE: This method is based on some intial experimentation
        # with OOo structural navigation.  It might need refining
        # or fixing and is being overridden by the Gecko method
        # regardless, so this one can be modified as appropriate.
        #
        if not ancestor or not ancestor.childCount:
            return ancestor

        lastChild = ancestor[ancestor.childCount - 1]
        while lastChild:
            lastObj = self._findNextObject(lastChild, ancestor)
            if lastObj:
                lastChild = lastObj
            else:
                break

        return lastChild

    def _getDocument(self):
        """Returns the document or other object in which the object of
        interest is contained.
        """

        docRoles = [pyatspi.ROLE_DOCUMENT_FRAME]
        stopRoles = [pyatspi.ROLE_FRAME, pyatspi.ROLE_SCROLL_PANE]
        document = self._script.utilities.ancestorWithRole(
            orca_state.locusOfFocus, docRoles, stopRoles)

        if not document and orca_state.locusOfFocus:
            if orca_state.locusOfFocus.getRole() in docRoles:
                return orca_state.locusOfFocus

        return document

    def _isInDocument(self, obj):
        """Returns True if the accessible object obj is inside of
        the document.

        Arguments:
        -obj: the accessible object of interest.
        """

        document = self._getDocument()
        while obj and obj.parent:
            if self._script.utilities.isSameObject(obj.parent, document):
                return True
            else:
                obj = obj.parent

        return False

    def _isUselessObject(self, obj):
        """Returns True if the accessible object obj is an object
        that doesn't have any meaning associated with it. Individual
        scripts should override this method as needed.  Gecko does.

        Arguments:
        - obj: the accessible object of interest.
        """

        return False
    #
    #
    # Methods for Presenting Objects                                        #
    #
    #

    def _getTableCaption(self, obj):
        """Returns a string which contains the table caption, or
        None if a caption could not be found.

        Arguments:
        - obj: the accessible table whose caption we want.
        """

        caption = obj.queryTable().caption
        try:
            caption.queryText()
        except:
            return None
        else:
            return self._script.utilities.displayedText(caption)

    def _getTableDescription(self, obj):
        """Returns a string which describes the table."""

        nonUniformString = ""
        nonUniform = self._isNonUniformTable(obj)
        if nonUniform:
            nonUniformString = messages.TABLE_NON_UNIFORM + " "

        table = obj.queryTable()
        sizeString = messages.tableSize(table.nRows, table.nColumns)
        return (nonUniformString + sizeString)

    def _isNonUniformTable(self, obj):
        """Returns True if the obj is a non-uniform table (i.e. a table
        where at least one cell spans multiple rows and/or columns).

        Arguments:
        - obj: the table to examine
        """

        try:
            table = obj.queryTable()
        except:
            pass
        else:
            for i in range(obj.childCount):
                [isCell, row, col, rowExtents, colExtents, isSelected] = \
                    table.getRowColumnExtentsAtIndex(i)
                if (rowExtents > 1) or (colExtents > 1):
                    return True

        return False

    def getCellForObj(self, obj):
        """Looks for a table cell in the ancestry of obj, if obj is not a
        table cell.

        Arguments:
        - obj: the accessible object of interest.
        """

        cellRoles = [pyatspi.ROLE_TABLE_CELL,
                     pyatspi.ROLE_COLUMN_HEADER,
                     pyatspi.ROLE_ROW_HEADER]
        if obj and not obj.getRole() in cellRoles:
            document = self._getDocument()
            obj = self._script.utilities.ancestorWithRole(
                obj, cellRoles, [document.getRole()])
        return obj

    def getTableForCell(self, obj):
        """Looks for a table in the ancestry of obj, if obj is not a table.

        Arguments:
        - obj: the accessible object of interest.
        """

        if obj and obj.getRole() != pyatspi.ROLE_TABLE:
            document = self._getDocument()
            obj = self._script.utilities.ancestorWithRole(
                obj, [pyatspi.ROLE_TABLE], [document.getRole()])
        return obj

    def _isBlankCell(self, obj):
        """Returns True if the table cell is empty or consists of whitespace.

        Arguments:
        - obj: the accessible table cell to examime
        """

        if obj and obj.name:
            return False

        text = self._script.utilities.displayedText(obj)
        if text and len(text.strip()) and text != obj.name:
            return False
        else:
            for child in obj:
                text = self._script.utilities.displayedText(child)
                if text and len(text.strip()) \
                   or child.getRole() == pyatspi.ROLE_LINK:
                    return False

        return True

    def _getCellText(self, obj):
        """Looks at the table cell and tries to get its text.

        Arguments:
        - obj: the accessible table cell to examime
        """

        text = ""
        if obj and not obj.childCount:
            text = self._script.utilities.displayedText(obj)
        else:
            for child in obj:
                childText = self._script.utilities.displayedText(child)
                text = self._script.utilities.appendString(text, childText)

        return text

    def _presentCellHeaders(self, cell, oldCellInfo):
        """Speaks the headers of the accessible table cell, cell.

        Arguments:
        - cell: the accessible table cell whose headers we wish to
          present.
        - oldCellInfo: [rowDiff, colDiff, oldRowHeaders, oldColHeaders]
        """

        if not cell or not oldCellInfo:
            return

        rowDiff, colDiff, oldRowHeaders, oldColHeaders = oldCellInfo
        if not (oldRowHeaders or oldColHeaders):
            return

        if rowDiff and not self._isInHeaderRow(cell):
            rowHeaders = self._getRowHeaders(cell)
            for header in rowHeaders:
                if not header in oldRowHeaders:
                    text = self._getCellText(header)
                    speech.speak(text)

        if colDiff:
            colHeaders = self._getColumnHeaders(cell)
            for header in colHeaders:
                if not header in oldColHeaders:
                    text = self._getCellText(header)
                    speech.speak(text)

    def _getCellSpanInfo(self, obj):
        """Returns a string reflecting the number of rows and/or columns
        spanned by a table cell when multiple rows and/or columns are
        spanned.

        Arguments:
        - obj: the accessible table cell whose cell span we want.
        """

        if not obj or (obj.getRole() != pyatspi.ROLE_TABLE_CELL):
            return

        parentTable = self.getTableForCell(obj)
        try:
            table = parentTable.queryTable()
        except:
            return

        [row, col] = self.getCellCoordinates(obj)
        rowspan = table.getRowExtentAt(row, col)
        colspan = table.getColumnExtentAt(row, col)
        return messages.cellSpan(rowspan, colspan)

    def getCellCoordinates(self, obj):
        """Returns the [row, col] of a ROLE_TABLE_CELL or [-1, -1]
        if the coordinates cannot be found.

        Arguments:
        - obj: the accessible table cell whose coordinates we want.
        """

        obj = self.getCellForObj(obj)
        parent = self.getTableForCell(obj)
        try:
            table = parent.queryTable()
        except:
            pass
        else:
            # If we're in a cell that spans multiple rows and/or columns,
            # thisRow and thisCol will refer to the upper left cell in
            # the spanned range(s).  We're storing the lastTableCell that
            # we're aware of in order to facilitate more linear movement.
            # Therefore, if the lastTableCell and this table cell are the
            # same cell, we'll go with the stored coordinates.
            #
            lastRow, lastCol = self.lastTableCell
            lastKnownCell = table.getAccessibleAt(lastRow, lastCol)
            if self._script.utilities.isSameObject(lastKnownCell, obj):
                return [lastRow, lastCol]
            else:
                index = self._script.utilities.cellIndex(obj)
                thisRow = table.getRowAtIndex(index)
                thisCol = table.getColumnAtIndex(index)
                return [thisRow, thisCol]

        return [-1, -1]

    def _getRowHeaders(self, obj):
        """Returns a list of table cells that serve as a row header for
        the specified TABLE_CELL.

        Arguments:
        - obj: the accessible table cell whose header(s) we want.
        """

        rowHeaders = []
        if not obj:
            return rowHeaders

        parentTable = self.getTableForCell(obj)
        try:
            table = parentTable.queryTable()
        except:
            pass
        else:
            [row, col] = self.getCellCoordinates(obj)
            # Theoretically, we should be able to quickly get the text
            # of a {row, column}Header via get{Row,Column}Description().
            # Gecko doesn't expose the information that way, however.
            # get{Row,Column}Header seems to work sometimes.
            #
            header = table.getRowHeader(row)
            if header:
                rowHeaders.append(header)

            # Headers that are strictly marked up with <th> do not seem
            # to be exposed through get{Row, Column}Header.
            #
            else:
                # If our cell spans multiple rows, we want to get all of
                # the headers that apply.
                #
                rowspan = table.getRowExtentAt(row, col)
                for r in range(row, row + rowspan):
                    # We could have multiple headers for a given row, one
                    # header per column.  Presumably all of the headers are
                    # prior to our present location.
                    #
                    for c in range(0, col):
                        cell = table.getAccessibleAt(r, c)
                        if self._isHeader(cell) and not cell in rowHeaders:
                            rowHeaders.append(cell)

        return rowHeaders

    def _getColumnHeaders(self, obj):
        """Returns a list of table cells that serve as a column header for
        the specified TABLE_CELL.

        Arguments:
        - obj: the accessible table cell whose header(s) we want.
        """

        columnHeaders = []
        if not obj:
            return columnHeaders

        parentTable = self.getTableForCell(obj)
        try:
            table = parentTable.queryTable()
        except:
            pass
        else:
            [row, col] = self.getCellCoordinates(obj)
            # Theoretically, we should be able to quickly get the text
            # of a {row, column}Header via get{Row,Column}Description().
            # Gecko doesn't expose the information that way, however.
            # get{Row,Column}Header seems to work sometimes.
            #
            header = table.getColumnHeader(col)
            if header:
                columnHeaders.append(header)

            # Headers that are strictly marked up with <th> do not seem
            # to be exposed through get{Row, Column}Header.
            #
            else:
                # If our cell spans multiple columns, we want to get all of
                # the headers that apply.
                #
                colspan = table.getColumnExtentAt(row, col)
                for c in range(col, col + colspan):
                    # We could have multiple headers for a given column, one
                    # header per row.  Presumably all of the headers are
                    # prior to our present location.
                    #
                    for r in range(0, row):
                        cell = table.getAccessibleAt(r, c)
                        if self._isHeader(cell) and not cell in columnHeaders:
                            columnHeaders.append(cell)

        return columnHeaders

    def _isInHeaderRow(self, obj):
        """Returns True if all of the cells in the same row as this cell are
        headers.

        Arguments:
        - obj: the accessible table cell whose row is to be examined.
        """

        if obj and obj.getRole() == pyatspi.ROLE_TABLE_CELL:
            parentTable = self.getTableForCell(obj)
            try:
                table = parentTable.queryTable()
            except:
                return True

            index = self._script.utilities.cellIndex(obj)
            row = table.getRowAtIndex(index)
            for col in range(table.nColumns):
                cell = table.getAccessibleAt(row, col)
                if not self._isHeader(cell):
                    return False

        return True

    def _isInHeaderColumn(self, obj):
        """Returns True if all of the cells in the same column as this cell
        are headers.

        Arguments:
        - obj: the accessible table cell whose column is to be examined.
        """

        if obj and obj.getRole() == pyatspi.ROLE_TABLE_CELL:
            parentTable = self.getTableForCell(obj)
            try:
                table = parentTable.queryTable()
            except:
                return True

            index = self._script.utilities.cellIndex(obj)
            col = table.getColumnAtIndex(index)
            for row in range(table.nRows):
                cell = table.getAccessibleAt(row, col)
                if not self._isHeader(cell):
                    return False

        return True

    def _isHeader(self, obj):
        """Returns True if the table cell is a header.

        Arguments:
        - obj: the accessible table cell to examine.
        """

        if not obj:
            return False

        elif obj.getRole() in [pyatspi.ROLE_TABLE_COLUMN_HEADER,
                               pyatspi.ROLE_TABLE_ROW_HEADER,
                               pyatspi.ROLE_COLUMN_HEADER,
                               pyatspi.ROLE_ROW_HEADER]:
            return True

        else:
            attributes = obj.getAttributes()
            if attributes:
                for attribute in attributes:
                    if attribute == "tag:TH":
                        return True

        return False

    def _getHeadingLevel(self, obj):
        """Determines the heading level of the given object.  A value
        of 0 means there is no heading level.

        Arguments:
        - obj: the accessible whose heading level we want.
        """

        level = 0

        if obj is None:
            return level

        if obj.getRole() == pyatspi.ROLE_HEADING:
            attributes = obj.getAttributes()
            if attributes is None:
                return level
            for attribute in attributes:
                if attribute.startswith("level:"):
                    level = int(attribute.split(":")[1])
                    break

        return level

    def _getCaretPosition(self, obj):
        """Returns the [obj, characterOffset] where the caret should be
        positioned. For most scripts, the object should not change and
        the offset should be 0.  That's not always the case with Gecko.

        Arguments:
        - obj: the accessible object in which the caret should be
          positioned.
        """

        return [obj, 0]

    def _setCaretPosition(self, obj, characterOffset):
        """Sets the caret at the specified offset within obj.

        Arguments:
        - obj: the accessible object in which the caret should be
          positioned.
        - characterOffset: the offset at which to position the caret.
        """

        try:
            text = obj.queryText()
            text.setCaretOffset(characterOffset)
        except NotImplementedError:
            try:
                obj.queryComponent().grabFocus()
            except:
                debug.printException(debug.LEVEL_SEVERE)
        except:
            debug.printException(debug.LEVEL_SEVERE)

        orca.setLocusOfFocus(None, obj, notifyScript=False)

    def _presentLine(self, obj, offset):
        """Presents the first line of the object to the user.

        Arguments:
        - obj: the accessible object to be presented.
        - offset: the character offset within obj.
        """

        self._script.updateBraille(obj)
        self._script.sayLine(obj)

    def _presentObject(self, obj, offset):
        """Presents the entire object to the user.

        Arguments:
        - obj: the accessible object to be presented.
        - offset: the character offset within obj.
        """

        self._script.updateBraille(obj)
        voices = self._script.voices
        if obj.getRole() == pyatspi.ROLE_LINK:
            voice = voices[settings.HYPERLINK_VOICE]
        else:
            voice = voices[settings.DEFAULT_VOICE]

        utterances = self._script.speechGenerator.generateSpeech(obj)
        speech.speak(utterances, voice)

    def _getRoleName(self, obj):
        # Another case where we'll do this for now, and clean it up when
        # object presentation is refactored.
        return self._script.speechGenerator.getLocalizedRoleName(obj)

    def _getSelectedItem(self, obj):
        # Another case where we'll do this for now, and clean it up when
        # object presentation is refactored.
        if obj.getRole() == pyatspi.ROLE_COMBO_BOX:
            obj = obj[0]
        try:
            selection = obj.querySelection()
        except NotImplementedError:
            return None

        return selection.getSelectedChild(0)

    def _getText(self, obj):
        # Another case where we'll do this for now, and clean it up when
        # object presentation is refactored.
        text = self._script.utilities.displayedText(obj)
        if not text:
            text = self._script.utilities.expandEOCs(obj)
        if not text:
            item = self._getSelectedItem(obj)
            if item:
                text = item.name

        return text

    def _getLabel(self, obj):
        # Another case where we'll do this for now, and clean it up when
        # object presentation is refactored.
        label = self._script.utilities.displayedLabel(obj)
        if not label:
            label = self._script.labelInference.infer(obj, focusedOnly=False)

        return label

    def _getState(self, obj):
        # Another case where we'll do this for now, and clean it up when
        # object presentation is refactored.
        try:
            state = obj.getState()
            role = obj.getRole()
        except RuntimeError:
            return ''

        # For now, we'll just grab the spoken indicator from settings.
        # When object presentation is refactored, we can clean this up.
        if role == pyatspi.ROLE_CHECK_BOX:
            unchecked, checked, partially = (object_properties.
                CHECK_BOX_INDICATORS_SPEECH)
            if state.contains(pyatspi.STATE_INDETERMINATE):
                return partially
            if state.contains(pyatspi.STATE_CHECKED):
                return checked
            return unchecked

        if role == pyatspi.ROLE_RADIO_BUTTON:
            unselected, selected = (object_properties.
                RADIO_BUTTON_INDICATORS_SPEECH)
            if state.contains(pyatspi.STATE_CHECKED):
                return selected
            return unselected

        if role == pyatspi.ROLE_LINK:
            if state.contains(pyatspi.STATE_VISITED):
                return object_properties.STATE_VISITED
            else:
                return object_properties.STATE_UNVISITED

        return ''

    def _getValue(self, obj):
        # Another case where we'll do this for now, and clean it up when
        # object presentation is refactored.
        return self._getState(obj) or self._getText(obj)
    #
    #
    # Objects                                                               #
    #
    #

    # All structural navigation objects have the following essential
    # characteristics:
    #
    # 1. Keybindings for goPrevious, goNext, and other such methods
    # 2. A means of identification (at least a predicate and possibly
    #    also criteria for generating a collection match rule)
    # 3. A definition of how the object should be presented (both
    #    when another instance of that object is found as well as
    #    when it is not)
    #
    # Convenience methods have been put into place whereby one can
    # create an object (FOO = "foo"), and then provide the following
    # methods: _fooBindings(), _fooPredicate(), _fooCriteria(), and
    # _fooPresentation().  With these in place, and with the object
    # FOO included among the StructuralNavigation.enabledTypes for
    # the script, the structural navigation object should be created
    # and set up automagically. At least that is the idea. :-) This
    # hopefully will also enable easy re-definition of existing
    # objects on a script-by-script basis.  For instance, in the
    # StarOffice script, overriding the _blockquotePredicate should
    # be all that is needed to implement navigation by blockquote
    # in OOo Writer documents.
    #

    #
    #
    # Anchors              #
    #
    #

    def _anchorBindings(self):
        """Returns a dictionary of [keysymstring, modifiers, description]
        lists for navigating amongst anchors.
        """
        # NOTE: This doesn't handle the case where the anchor is not an
        # old-school <a name/id="foo"></a> anchor. For instance on the
        # GNOME wiki, an "anchor" is actually an id applied to some other
        # tag (e.g. <h2 id="foo">My Heading</h2>.  We'll have to be a
        # bit more clever for those.  With the old-school anchors, this
        # seems to work nicely and provides the user with a way to jump
        # among defined areas without having to find a Table of Contents
        # group of links (assuming such a thing is even present on the
        # page).

        bindings = {}
        prevDesc = cmdnames.ANCHOR_PREV
        bindings["previous"] = ["a", settings.SHIFT_MODIFIER_MASK, prevDesc]

        nextDesc = cmdnames.ANCHOR_NEXT
        bindings["next"] = ["a", settings.NO_MODIFIER_MASK, nextDesc]
        return bindings

    def _anchorCriteria(self, collection, arg=None):
        """Returns the MatchCriteria to be used for locating anchors
        by collection.

        Arguments:
        - collection: the collection interface for the document
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        role = [pyatspi.ROLE_LINK]
        state = [pyatspi.STATE_FOCUSABLE]
        stateMatch = collection.MATCH_NONE
        return MatchCriteria(collection,
                             states=state,
                             matchStates=stateMatch,
                             roles=role)

    def _anchorPredicate(self, obj, arg=None):
        """The predicate to be used for verifying that the object
        obj is an anchor.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        isMatch = False
        if obj and obj.getRole() == pyatspi.ROLE_LINK:
            state = obj.getState()
            isMatch = not state.contains(pyatspi.STATE_FOCUSABLE)
        return isMatch

    def _anchorPresentation(self, obj, arg=None):
        """Presents the anchor or indicates that one was not found.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        if obj:
            [obj, characterOffset] = self._getCaretPosition(obj)
            self._setCaretPosition(obj, characterOffset)
            self._presentObject(obj, characterOffset)
        else:
            full = messages.NO_MORE_ANCHORS
            brief = messages.STRUCTURAL_NAVIGATION_NOT_FOUND
            self._script.presentMessage(full, brief)
    #
    #
    # Blockquotes          #
    #
    #

    def _blockquoteBindings(self):
        """Returns a dictionary of [keysymstring, modifiers, description]
        lists for navigating among blockquotes.
        """

        bindings = {}
        prevDesc = cmdnames.BLOCKQUOTE_PREV
        bindings["previous"] = ["q", settings.SHIFT_MODIFIER_MASK, prevDesc]

        nextDesc = cmdnames.BLOCKQUOTE_NEXT
        bindings["next"] = ["q", settings.NO_MODIFIER_MASK, nextDesc]

        listDesc = cmdnames.BLOCKQUOTE_LIST
        bindings["list"] = ["q", settings.SHIFT_ALT_MODIFIER_MASK, listDesc]
        return bindings

    def _blockquoteCriteria(self, collection, arg=None):
        """Returns the MatchCriteria to be used for locating blockquotes
        by collection.

        Arguments:
        - collection: the collection interface for the document
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        attrs = ['tag:BLOCKQUOTE']
        return MatchCriteria(collection, objAttrs=attrs)

    def _blockquotePredicate(self, obj, arg=None):
        """The predicate to be used for verifying that the object
        obj is a blockquote.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        if not obj:
            return False

        attributes = obj.getAttributes()
        if attributes:
            for attribute in attributes:
                if attribute == "tag:BLOCKQUOTE":
                    return True

        return False

    def _blockquotePresentation(self, obj, arg=None):
        """Presents the blockquote or indicates that one was not found.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        if obj:
            [obj, characterOffset] = self._getCaretPosition(obj)
            self._setCaretPosition(obj, characterOffset)
            # TODO: We currently present the line, so that's kept here.
            # But we should probably present the object, which would
            # be consistent with the change made recently for headings.
            #
            self._presentLine(obj, characterOffset)
        else:
            full = messages.NO_MORE_BLOCKQUOTES
            brief = messages.STRUCTURAL_NAVIGATION_NOT_FOUND
            self._script.presentMessage(full, brief)

    def _blockquoteDialogData(self):
        columnHeaders = [guilabels.SN_HEADER_BLOCKQUOTE]

        def rowData(obj):
            return [self._getText(obj)]

        return guilabels.SN_TITLE_BLOCKQUOTE, columnHeaders, rowData
    #
    #
    # Buttons              #
    #
    #

    def _buttonBindings(self):
        """Returns a dictionary of [keysymstring, modifiers, description]
        lists for navigating amongst buttons.
        """

        bindings = {}
        prevDesc = cmdnames.BUTTON_PREV
        bindings["previous"] = ["b", settings.SHIFT_MODIFIER_MASK, prevDesc]

        nextDesc = cmdnames.BUTTON_NEXT
        bindings["next"] = ["b", settings.NO_MODIFIER_MASK, nextDesc]

        listDesc = cmdnames.BUTTON_LIST
        bindings["list"] = ["b", settings.SHIFT_ALT_MODIFIER_MASK, listDesc]
        return bindings

    def _buttonCriteria(self, collection, arg=None):
        """Returns the MatchCriteria to be used for locating buttons
        by collection.

        Arguments:
        - collection: the collection interface for the document
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        role = [pyatspi.ROLE_PUSH_BUTTON]
        state = [pyatspi.STATE_FOCUSABLE, pyatspi.STATE_SENSITIVE]
        stateMatch = collection.MATCH_ALL
        return MatchCriteria(collection,
                             states=state,
                             matchStates=stateMatch,
                             roles=role)

    def _buttonPredicate(self, obj, arg=None):
        """The predicate to be used for verifying that the object
        obj is a button.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        isMatch = False
        if obj and obj.getRole() == pyatspi.ROLE_PUSH_BUTTON:
            state = obj.getState()
            isMatch = state.contains(pyatspi.STATE_FOCUSABLE) \
                and state.contains(pyatspi.STATE_SENSITIVE)

        return isMatch

    def _buttonPresentation(self, obj, arg=None):
        """Presents the button or indicates that one was not found.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        if obj:
            obj.queryComponent().grabFocus()
        else:
            full = messages.NO_MORE_BUTTONS
            brief = messages.STRUCTURAL_NAVIGATION_NOT_FOUND
            self._script.presentMessage(full, brief)

    def _buttonDialogData(self):
        columnHeaders = [guilabels.SN_HEADER_BUTTON]

        def rowData(obj):
            return [self._getText(obj)]

        return guilabels.SN_TITLE_BUTTON, columnHeaders, rowData
    #
    #
    # Check boxes          #
    #
    #

    def _checkBoxBindings(self):
        """Returns a dictionary of [keysymstring, modifiers, description]
        lists for navigating amongst check boxes.
        """

        bindings = {}
        prevDesc = cmdnames.CHECK_BOX_PREV
        bindings["previous"] = ["x", settings.SHIFT_MODIFIER_MASK, prevDesc]

        nextDesc = cmdnames.CHECK_BOX_NEXT
        bindings["next"] = ["x", settings.NO_MODIFIER_MASK, nextDesc]

        listDesc = cmdnames.CHECK_BOX_LIST
        bindings["list"] = ["x", settings.SHIFT_ALT_MODIFIER_MASK, listDesc]
        return bindings

    def _checkBoxCriteria(self, collection, arg=None):
        """Returns the MatchCriteria to be used for locating check boxes
        by collection.

        Arguments:
        - collection: the collection interface for the document
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        role = [pyatspi.ROLE_CHECK_BOX]
        state = [pyatspi.STATE_FOCUSABLE, pyatspi.STATE_SENSITIVE]
        stateMatch = collection.MATCH_ALL
        return MatchCriteria(collection,
                             states=state,
                             matchStates=stateMatch,
                             roles=role)

    def _checkBoxPredicate(self, obj, arg=None):
        """The predicate to be used for verifying that the object
        obj is a check box.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        isMatch = False
        if obj and obj.getRole() == pyatspi.ROLE_CHECK_BOX:
            state = obj.getState()
            isMatch = state.contains(pyatspi.STATE_FOCUSABLE) \
                and state.contains(pyatspi.STATE_SENSITIVE)

        return isMatch

    def _checkBoxPresentation(self, obj, arg=None):
        """Presents the check box or indicates that one was not found.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        if obj:
            obj.queryComponent().grabFocus()
        else:
            full = messages.NO_MORE_CHECK_BOXES
            brief = messages.STRUCTURAL_NAVIGATION_NOT_FOUND
            self._script.presentMessage(full, brief)

    def _checkBoxDialogData(self):
        columnHeaders = [guilabels.SN_HEADER_CHECK_BOX]
        columnHeaders.append(guilabels.SN_HEADER_STATE)

        def rowData(obj):
            return [self._getLabel(obj), self._getState(obj)]

        return guilabels.SN_TITLE_CHECK_BOX, columnHeaders, rowData
    #
    #
    # Chunks/Large Objects #
    #
    #

    def _chunkBindings(self):
        """Returns a dictionary of [keysymstring, modifiers, description]
        lists for navigating amongst chunks/large objects.
        """

        bindings = {}
        prevDesc = cmdnames.LARGE_OBJECT_PREV
        bindings["previous"] = ["o", settings.SHIFT_MODIFIER_MASK, prevDesc]

        nextDesc = cmdnames.LARGE_OBJECT_NEXT
        bindings["next"] = ["o", settings.NO_MODIFIER_MASK, nextDesc]

        listDesc = cmdnames.LARGE_OBJECT_LIST
        bindings["list"] = ["o", settings.SHIFT_ALT_MODIFIER_MASK, listDesc]
        return bindings

    def _chunkCriteria(self, collection, arg=None):
        """Returns the MatchCriteria to be used for locating chunks/
        large objects by collection.

        Arguments:
        - collection: the collection interface for the document
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        role = self.OBJECT_ROLES
        roleMatch = collection.MATCH_ANY
        return MatchCriteria(collection,
                             roles=role,
                             matchRoles=roleMatch,
                             applyPredicate=True)

    def _chunkPredicate(self, obj, arg=None):
        """The predicate to be used for verifying that the object
        obj is a chunk.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        isMatch = False

        if obj and obj.getRole() in self.OBJECT_ROLES:
            try:
                text = obj.queryText()
                characterCount = text.characterCount
            except:
                characterCount = 0

            if characterCount > settings.largeObjectTextLength \
               and not self._isUselessObject(obj):
                isMatch = True

        return isMatch

    def _chunkPresentation(self, obj, arg=None):
        """Presents the chunk or indicates that one was not found.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        if obj:
            [newObj, characterOffset] = self._getCaretPosition(obj)
            self._setCaretPosition(newObj, characterOffset)
            self._presentObject(obj, 0)
        else:
            full = messages.NO_MORE_CHUNKS
            brief = messages.STRUCTURAL_NAVIGATION_NOT_FOUND
            self._script.presentMessage(full, brief)

    def _chunkDialogData(self):
        columnHeaders = [guilabels.SN_HEADER_OBJECT]
        columnHeaders.append(guilabels.SN_HEADER_ROLE)

        def rowData(obj):
            return [self._getText(obj), self._getRoleName(obj)]

        return guilabels.SN_TITLE_LARGE_OBJECT, columnHeaders, rowData
    #
    #
    # Combo Boxes          #
    #
    #

    def _comboBoxBindings(self):
        """Returns a dictionary of [keysymstring, modifiers, description]
        lists for navigating amongst combo boxes.
        """

        bindings = {}
        prevDesc = cmdnames.COMBO_BOX_PREV
        bindings["previous"] = ["c", settings.SHIFT_MODIFIER_MASK, prevDesc]

        nextDesc = cmdnames.COMBO_BOX_NEXT
        bindings["next"] = ["c", settings.NO_MODIFIER_MASK, nextDesc]

        listDesc = cmdnames.COMBO_BOX_LIST
        bindings["list"] = ["c", settings.SHIFT_ALT_MODIFIER_MASK, listDesc]
        return bindings

    def _comboBoxCriteria(self, collection, arg=None):
        """Returns the MatchCriteria to be used for locating combo boxes
        by collection.

        Arguments:
        - collection: the collection interface for the document
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        role = [pyatspi.ROLE_COMBO_BOX]
        state = [pyatspi.STATE_FOCUSABLE, pyatspi.STATE_SENSITIVE]
        stateMatch = collection.MATCH_ALL
        return MatchCriteria(collection,
                             states=state,
                             matchStates=stateMatch,
                             roles=role)

    def _comboBoxPredicate(self, obj, arg=None):
        """The predicate to be used for verifying that the object
        obj is a combo box.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        isMatch = False
        if obj and obj.getRole() == pyatspi.ROLE_COMBO_BOX:
            state = obj.getState()
            isMatch = state.contains(pyatspi.STATE_FOCUSABLE) \
                and state.contains(pyatspi.STATE_SENSITIVE)

        return isMatch

    def _comboBoxPresentation(self, obj, arg=None):
        """Presents the combo box or indicates that one was not found.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        if obj:
            obj.queryComponent().grabFocus()
        else:
            full = messages.NO_MORE_COMBO_BOXES
            brief = messages.STRUCTURAL_NAVIGATION_NOT_FOUND
            self._script.presentMessage(full, brief)

    def _comboBoxDialogData(self):
        columnHeaders = [guilabels.SN_HEADER_COMBO_BOX]
        columnHeaders.append(guilabels.SN_HEADER_SELECTED_ITEM)

        def rowData(obj):
            return [self._getLabel(obj), self._getText(obj)]

        return guilabels.SN_TITLE_COMBO_BOX, columnHeaders, rowData
    #
    #
    # Entries              #
    #
    #

    def _entryBindings(self):
        """Returns a dictionary of [keysymstring, modifiers, description]
        lists for navigating amongst entries.
        """

        bindings = {}
        prevDesc = cmdnames.ENTRY_PREV
        bindings["previous"] = ["e", settings.SHIFT_MODIFIER_MASK, prevDesc]

        nextDesc = cmdnames.ENTRY_NEXT
        bindings["next"] = ["e", settings.NO_MODIFIER_MASK, nextDesc]

        listDesc = cmdnames.ENTRY_LIST
        bindings["list"] = ["e", settings.SHIFT_ALT_MODIFIER_MASK, listDesc]
        return bindings

    def _entryCriteria(self, collection, arg=None):
        """Returns the MatchCriteria to be used for locating entries
        by collection.

        Arguments:
        - collection: the collection interface for the document
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        role = [pyatspi.ROLE_DOCUMENT_FRAME,
                pyatspi.ROLE_ENTRY,
                pyatspi.ROLE_PASSWORD_TEXT,
                pyatspi.ROLE_TEXT]
        roleMatch = collection.MATCH_ANY
        state = [pyatspi.STATE_FOCUSABLE,
                 pyatspi.STATE_SENSITIVE,
                 pyatspi.STATE_EDITABLE]
        stateMatch = collection.MATCH_ALL
        return MatchCriteria(collection,
                             states=state,
                             matchStates=stateMatch,
                             roles=role,
                             matchRoles=roleMatch,
                             applyPredicate=True)

    def _entryPredicate(self, obj, arg=None):
        """The predicate to be used for verifying that the object
        obj is an entry.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        isMatch = False
        if obj and obj.getRole() in [pyatspi.ROLE_DOCUMENT_FRAME,
                                     pyatspi.ROLE_ENTRY,
                                     pyatspi.ROLE_PASSWORD_TEXT,
                                     pyatspi.ROLE_TEXT]:
            state = obj.getState()
            isMatch = state.contains(pyatspi.STATE_FOCUSABLE) \
                and state.contains(pyatspi.STATE_SENSITIVE) \
                and state.contains(pyatspi.STATE_EDITABLE)

        return isMatch

    def _entryPresentation(self, obj, arg=None):
        """Presents the entry or indicates that one was not found.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        if obj:
            obj.queryComponent().grabFocus()
        else:
            full = messages.NO_MORE_ENTRIES
            brief = messages.STRUCTURAL_NAVIGATION_NOT_FOUND
            self._script.presentMessage(full, brief)

    def _entryDialogData(self):
        columnHeaders = [guilabels.SN_HEADER_LABEL]
        columnHeaders.append(guilabels.SN_HEADER_TEXT)

        def rowData(obj):
            return [self._getLabel(obj), self._getText(obj)]

        return guilabels.SN_TITLE_ENTRY, columnHeaders, rowData
    #
    #
    # Form Fields          #
    #
    #

    def _formFieldBindings(self):
        """Returns a dictionary of [keysymstring, modifiers, description]
        lists for navigating amongst form fields.
        """

        bindings = {}
        prevDesc = cmdnames.FORM_FIELD_PREV
        bindings["previous"] = ["Tab",
                                settings.ORCA_SHIFT_MODIFIER_MASK,
                                prevDesc]

        nextDesc = cmdnames.FORM_FIELD_NEXT
        bindings["next"] = ["Tab", settings.ORCA_MODIFIER_MASK, nextDesc]

        listDesc = cmdnames.FORM_FIELD_LIST
        bindings["list"] = ["f", settings.SHIFT_ALT_MODIFIER_MASK, listDesc]
        return bindings

    def _formFieldCriteria(self, collection, arg=None):
        """Returns the MatchCriteria to be used for locating form fields
        by collection.

        Arguments:
        - collection: the collection interface for the document
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        role = self.FORM_ROLES
        roleMatch = collection.MATCH_ANY
        state = [pyatspi.STATE_FOCUSABLE, pyatspi.STATE_SENSITIVE]
        stateMatch = collection.MATCH_ALL
        return MatchCriteria(collection,
                             states=state,
                             matchStates=stateMatch,
                             roles=role,
                             matchRoles=roleMatch,
                             applyPredicate=True)

    def _formFieldPredicate(self, obj, arg=None):
        """The predicate to be used for verifying that the object
        obj is a form field.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        isMatch = False
        if obj and obj.getRole() in self.FORM_ROLES:
            state = obj.getState()
            isMatch = state.contains(pyatspi.STATE_FOCUSABLE) \
                and state.contains(pyatspi.STATE_SENSITIVE)

        return isMatch

    def _formFieldPresentation(self, obj, arg=None):
        """Presents the form field or indicates that one was not found.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        if obj:
            if obj.getRole() == pyatspi.ROLE_TEXT and obj.childCount:
                obj = obj[0]
            obj.queryComponent().grabFocus()
        else:
            full = messages.NO_MORE_FORM_FIELDS
            brief = messages.STRUCTURAL_NAVIGATION_NOT_FOUND
            self._script.presentMessage(full, brief)

    def _formFieldDialogData(self):
        columnHeaders = [guilabels.SN_HEADER_LABEL]
        columnHeaders.append(guilabels.SN_HEADER_ROLE)
        columnHeaders.append(guilabels.SN_HEADER_VALUE)

        def rowData(obj):
            return [self._getLabel(obj),
                    self._getRoleName(obj),
                    self._getValue(obj)]

        return guilabels.SN_TITLE_FORM_FIELD, columnHeaders, rowData
    #
    #
    # Headings             #
    #
    #

    def _headingBindings(self):
        """Returns a dictionary of [keysymstring, modifiers, description]
        lists for navigating amongst headings.
        """

        bindings = {}
        prevDesc = cmdnames.HEADING_PREV
        bindings["previous"] = ["h", settings.SHIFT_MODIFIER_MASK, prevDesc]

        nextDesc = cmdnames.HEADING_NEXT
        bindings["next"] = ["h", settings.NO_MODIFIER_MASK, nextDesc]

        listDesc = cmdnames.HEADING_LIST
        bindings["list"] = ["h", settings.SHIFT_ALT_MODIFIER_MASK, listDesc]

        prevAtLevelBindings = []
        nextAtLevelBindings = []
        listAtLevelBindings = []
        minLevel, maxLevel = self._headingLevels()
        for i in range(minLevel, maxLevel + 1):
            prevDesc = cmdnames.HEADING_AT_LEVEL_PREV % i
            prevAtLevelBindings.append([str(i),
                                        settings.SHIFT_MODIFIER_MASK,
                                        prevDesc])

            nextDesc = cmdnames.HEADING_AT_LEVEL_NEXT % i
            nextAtLevelBindings.append([str(i),
                                        settings.NO_MODIFIER_MASK,
                                        nextDesc])

            listDesc = cmdnames.HEADING_AT_LEVEL_LIST % i
            listAtLevelBindings.append([str(i),
                                        settings.SHIFT_ALT_MODIFIER_MASK,
                                        listDesc])

        bindings["previousAtLevel"] = prevAtLevelBindings
        bindings["nextAtLevel"] = nextAtLevelBindings
        bindings["listAtLevel"] = listAtLevelBindings

        return bindings

    def _headingLevels(self):
        """Returns the [minimum heading level, maximum heading level]
        which should be navigable via structural navigation.
        """

        return [1, 6]

    def _headingCriteria(self, collection, arg=None):
        """Returns the MatchCriteria to be used for locating headings
        by collection.

        Arguments:
        - collection: the collection interface for the document
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        role = [pyatspi.ROLE_HEADING]
        attrs = []
        if arg:
            attrs.append('level:%d' % arg)

        return MatchCriteria(collection,
                             roles=role,
                             objAttrs=attrs)

    def _headingPredicate(self, obj, arg=None):
        """The predicate to be used for verifying that the object
        obj is a heading.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        isMatch = False
        if obj and obj.getRole() == pyatspi.ROLE_HEADING:
            if arg:
                isMatch = (arg == self._getHeadingLevel(obj))
            else:
                isMatch = True

        return isMatch

    def _headingPresentation(self, obj, arg=None):
        """Presents the heading or indicates that one was not found.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        if obj:
            [obj, characterOffset] = self._getCaretPosition(obj)
            self._setCaretPosition(obj, characterOffset)
            self._presentObject(obj, characterOffset)
        elif not arg:
            full = messages.NO_MORE_HEADINGS
            brief = messages.STRUCTURAL_NAVIGATION_NOT_FOUND
            self._script.presentMessage(full, brief)
        else:
            full = messages.NO_MORE_HEADINGS_AT_LEVEL % arg
            brief = messages.STRUCTURAL_NAVIGATION_NOT_FOUND
            self._script.presentMessage(full, brief)

    def _headingDialogData(self, arg=None):
        columnHeaders = [guilabels.SN_HEADER_HEADING]

        if not arg:
            title = guilabels.SN_TITLE_HEADING
            columnHeaders.append(guilabels.SN_HEADER_LEVEL)

            def rowData(obj):
                return [self._getText(obj), str(self._getHeadingLevel(obj))]

        else:
            title = guilabels.SN_TITLE_HEADING_AT_LEVEL % arg

            def rowData(obj):
                return [self._getText(obj)]

        return title, columnHeaders, rowData
    #
    #
    # Landmarks            #
    #
    #

    def _landmarkBindings(self):
        """Returns a dictionary of [keysymstring, modifiers, description]
        lists for navigating amongst landmarks.
        """

        bindings = {}
        prevDesc = cmdnames.LANDMARK_PREV
        bindings["previous"] = ["m", settings.SHIFT_MODIFIER_MASK, prevDesc]

        nextDesc = cmdnames.LANDMARK_NEXT
        bindings["next"] = ["m", settings.NO_MODIFIER_MASK, nextDesc]

        listDesc = cmdnames.LANDMARK_LIST
        bindings["list"] = ["m", settings.SHIFT_ALT_MODIFIER_MASK, listDesc]
        return bindings

    def _landmarkCriteria(self, collection, arg=None):
        """Returns the MatchCriteria to be used for locating landmarks
        by collection.

        Arguments:
        - collection: the collection interface for the document
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        # NOTE: there is a limitation in the AT-SPI Collections interface
        # when it comes to an attribute whose value can be a list.  For
        # example, the xml-roles attribute can be a space-separate list
        # of roles.  We'd like to make a match if the xml-roles attribute
        # has one (or any) of the roles we care about.  Instead, we're
        # restricted to an exact match.  So, the below will only work in
        # the cases where the xml-roles attribute value consists solely of a
        # single role.  In practice, this seems to be the case that we run
        # into for the landmark roles.
        #
        attrs = []
        for landmark in settings.ariaLandmarks:
            attrs.append('xml-roles:' + landmark)

        return MatchCriteria(collection, objAttrs=attrs)

    def _landmarkPredicate(self, obj, arg=None):
        """The predicate to be used for verifying that the object
        obj is a landmark.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        if obj is None:
            return False

        attrs = dict([attr.split(':', 1) for attr in obj.getAttributes()])
        try:
            if set(attrs['xml-roles']).intersection(
                    set(settings.ariaLandmarks)):
                return True
            else:
                return False
        except KeyError:
            return False

    def _landmarkPresentation(self, obj, arg=None):
        """Presents the landmark or indicates that one was not found.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        if obj:
            [obj, characterOffset] = self._getCaretPosition(obj)
            self._setCaretPosition(obj, characterOffset)
            self._presentObject(obj, characterOffset)
        else:
            full = messages.NO_LANDMARK_FOUND
            brief = messages.STRUCTURAL_NAVIGATION_NOT_FOUND
            self._script.presentMessage(full, brief)

    def _landmarkDialogData(self):
        columnHeaders = [guilabels.SN_HEADER_LANDMARK]

        def rowData(obj):
            return [self._getText(obj)]

        return guilabels.SN_TITLE_LANDMARK, columnHeaders, rowData
    #
    #
    # Lists                #
    #
    #

    def _listBindings(self):
        """Returns a dictionary of [keysymstring, modifiers, description]
        lists for navigating amongst (un)ordered lists.
        """

        bindings = {}
        prevDesc = cmdnames.LIST_PREV
        bindings["previous"] = ["l", settings.SHIFT_MODIFIER_MASK, prevDesc]

        nextDesc = cmdnames.LIST_NEXT
        bindings["next"] = ["l", settings.NO_MODIFIER_MASK, nextDesc]

        listDesc = cmdnames.LIST_LIST
        bindings["list"] = ["l", settings.SHIFT_ALT_MODIFIER_MASK, listDesc]
        return bindings

    def _listCriteria(self, collection, arg=None):
        """Returns the MatchCriteria to be used for locating (un)ordered
        lists by collection.

        Arguments:
        - collection: the collection interface for the document
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        role = [pyatspi.ROLE_LIST]
        state = [pyatspi.STATE_FOCUSABLE]
        stateMatch = collection.MATCH_NONE
        return MatchCriteria(collection,
                             states=state,
                             matchStates=stateMatch,
                             roles=role)

    def _listPredicate(self, obj, arg=None):
        """The predicate to be used for verifying that the object
        obj is an (un)ordered list.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        isMatch = False

        if obj and obj.getRole() == pyatspi.ROLE_LIST:
            isMatch = not obj.getState().contains(pyatspi.STATE_FOCUSABLE)

        return isMatch

    def _listPresentation(self, obj, arg=None):
        """Presents the (un)ordered list or indicates that one was not
        found.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        # TODO: Ultimately it should be the job of the speech (and braille)
        # generator to present things like this.
        #
        if obj:
            nItems = 0
            for child in obj:
                if child.getRole() == pyatspi.ROLE_LIST_ITEM:
                    nItems += 1
            self._script.presentMessage(messages.listItemCount(nItems))
            nestingLevel = 0
            parent = obj.parent
            while parent.getRole() == pyatspi.ROLE_LIST:
                nestingLevel += 1
                parent = parent.parent
            if nestingLevel:
                self._script.presentMessage(
                    messages.NESTING_LEVEL % nestingLevel)
            [obj, characterOffset] = self._getCaretPosition(obj)
            self._setCaretPosition(obj, characterOffset)
            self._presentLine(obj, characterOffset)
        else:
            full = messages.NO_MORE_LISTS
            brief = messages.STRUCTURAL_NAVIGATION_NOT_FOUND
            self._script.presentMessage(full, brief)

    def _listDialogData(self):
        columnHeaders = [guilabels.SN_HEADER_LIST]

        def rowData(obj):
            return [self._getText(obj)]

        return guilabels.SN_TITLE_LIST, columnHeaders, rowData
    #
    #
    # List Items           #
    #
    #

    def _listItemBindings(self):
        """Returns a dictionary of [keysymstring, modifiers, description]
        lists for navigating amongst items in an (un)ordered list.
        """

        bindings = {}
        prevDesc = cmdnames.LIST_ITEM_PREV
        bindings["previous"] = ["i", settings.SHIFT_MODIFIER_MASK, prevDesc]

        nextDesc = cmdnames.LIST_ITEM_NEXT
        bindings["next"] = ["i", settings.NO_MODIFIER_MASK, nextDesc]

        listDesc = cmdnames.LIST_ITEM_LIST
        bindings["list"] = ["i", settings.SHIFT_ALT_MODIFIER_MASK, listDesc]
        return bindings

    def _listItemCriteria(self, collection, arg=None):
        """Returns the MatchCriteria to be used for locating items in an
        (un)ordered list by collection.

        Arguments:
        - collection: the collection interface for the document
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        role = [pyatspi.ROLE_LIST_ITEM]
        state = [pyatspi.STATE_FOCUSABLE]
        stateMatch = collection.MATCH_NONE
        return MatchCriteria(collection,
                             states=state,
                             matchStates=stateMatch,
                             roles=role)

    def _listItemPredicate(self, obj, arg=None):
        """The predicate to be used for verifying that the object
        obj is an item in an (un)ordered list.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        isMatch = False

        if obj and obj.getRole() == pyatspi.ROLE_LIST_ITEM:
            isMatch = not obj.getState().contains(pyatspi.STATE_FOCUSABLE)

        return isMatch

    def _listItemPresentation(self, obj, arg=None):
        """Presents the (un)ordered list item or indicates that one was not
        found.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        if obj:
            [obj, characterOffset] = self._getCaretPosition(obj)
            self._setCaretPosition(obj, characterOffset)
            # TODO: We currently present the line, so that's kept here.
            # But we should probably present the object, which would
            # be consistent with the change made recently for headings.
            #
            self._presentLine(obj, characterOffset)
        else:
            full = messages.NO_MORE_LIST_ITEMS
            brief = messages.STRUCTURAL_NAVIGATION_NOT_FOUND
            self._script.presentMessage(full, brief)

    def _listItemDialogData(self):
        columnHeaders = [guilabels.SN_HEADER_LIST_ITEM]

        def rowData(obj):
            return [self._getText(obj)]

        return guilabels.SN_TITLE_LIST_ITEM, columnHeaders, rowData
    #
    #
    # Live Regions         #
    #
    #

    def _liveRegionBindings(self):
        """Returns a dictionary of [keysymstring, modifiers, description]
        lists for navigating amongst live regions.
        """

        bindings = {}
        prevDesc = cmdnames.LIVE_REGION_PREV
        bindings["previous"] = ["d", settings.SHIFT_MODIFIER_MASK, prevDesc]

        nextDesc = cmdnames.LIVE_REGION_NEXT
        bindings["next"] = ["d", settings.NO_MODIFIER_MASK, nextDesc]

        desc = cmdnames.LIVE_REGION_LAST
        bindings["last"] = ["y", settings.NO_MODIFIER_MASK, desc]
        return bindings

    def _liveRegionCriteria(self, collection, arg=None):
        """Returns the MatchCriteria to be used for locating live regions
        by collection.

        Arguments:
        - collection: the collection interface for the document
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        # Matches based on object attributes assume unique name-value pairs
        # because pyatspi creates a dictionary from the list. In addition,
        # wildcard matching is not possible. As a result, we cannot search
        # for any object which has an attribute named container-live.
        return MatchCriteria(collection, applyPredicate=True)

    def _liveRegionPredicate(self, obj, arg=None):
        """The predicate to be used for verifying that the object
        obj is a live region.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        isMatch = False

        regobjs = self._script.liveMngr.getLiveNoneObjects()
        if self._script.liveMngr.matchLiveRegion(obj) or obj in regobjs:
            isMatch = True

        return isMatch

    def _liveRegionPresentation(self, obj, arg=None):
        """Presents the live region or indicates that one was not found.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        if obj:
            # TODO: We don't want to move to a list item.
            # Is this the best place to handle this?
            #
            if obj.getRole() == pyatspi.ROLE_LIST:
                characterOffset = 0
            else:
                [obj, characterOffset] = self._getCaretPosition(obj)
            self._setCaretPosition(obj, characterOffset)
            self._presentObject(obj, characterOffset)
        else:
            full = messages.NO_MORE_LIVE_REGIONS
            brief = messages.STRUCTURAL_NAVIGATION_NOT_FOUND
            self._script.presentMessage(full, brief)
    #
    #
    # Paragraphs           #
    #
    #

    def _paragraphBindings(self):
        """Returns a dictionary of [keysymstring, modifiers, description]
        lists for navigating amongst paragraphs.
        """

        bindings = {}
        prevDesc = cmdnames.PARAGRAPH_PREV
        bindings["previous"] = ["p", settings.SHIFT_MODIFIER_MASK, prevDesc]

        nextDesc = cmdnames.PARAGRAPH_NEXT
        bindings["next"] = ["p", settings.NO_MODIFIER_MASK, nextDesc]

        listDesc = cmdnames.PARAGRAPH_LIST
        bindings["list"] = ["p", settings.SHIFT_ALT_MODIFIER_MASK, listDesc]
        return bindings

    def _paragraphCriteria(self, collection, arg=None):
        """Returns the MatchCriteria to be used for locating paragraphs
        by collection.

        Arguments:
        - collection: the collection interface for the document
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        role = [pyatspi.ROLE_PARAGRAPH]
        return MatchCriteria(collection, roles=role, applyPredicate=True)

    def _paragraphPredicate(self, obj, arg=None):
        """The predicate to be used for verifying that the object
        obj is a paragraph.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        isMatch = False
        if obj and obj.getRole() == pyatspi.ROLE_PARAGRAPH:
            try:
                text = obj.queryText()
                # We're choosing 3 characters as the minimum because some
                # paragraphs contain a single image or link and a text
                # of length 2: An embedded object character and a space.
                # We want to skip these.
                #
                isMatch = text.characterCount > 2
            except:
                pass

        return isMatch

    def _paragraphPresentation(self, obj, arg=None):
        """Presents the paragraph or indicates that one was not found.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        if obj:
            [newObj, characterOffset] = self._getCaretPosition(obj)
            self._setCaretPosition(newObj, characterOffset)
            self._presentObject(obj, 0)
        else:
            full = messages.NO_MORE_PARAGRAPHS
            brief = messages.STRUCTURAL_NAVIGATION_NOT_FOUND
            self._script.presentMessage(full, brief)

    def _paragraphDialogData(self):
        columnHeaders = [guilabels.SN_HEADER_PARAGRAPH]

        def rowData(obj):
            return [self._getText(obj)]

        return guilabels.SN_TITLE_PARAGRAPH, columnHeaders, rowData
    #
    #
    # Radio Buttons        #
    #
    #

    def _radioButtonBindings(self):
        """Returns a dictionary of [keysymstring, modifiers, description]
        lists for navigating amongst radio buttons.
        """

        bindings = {}
        prevDesc = cmdnames.RADIO_BUTTON_PREV
        bindings["previous"] = ["r", settings.SHIFT_MODIFIER_MASK, prevDesc]

        nextDesc = cmdnames.RADIO_BUTTON_NEXT
        bindings["next"] = ["r", settings.NO_MODIFIER_MASK, nextDesc]

        listDesc = cmdnames.RADIO_BUTTON_LIST
        bindings["list"] = ["r", settings.SHIFT_ALT_MODIFIER_MASK, listDesc]
        return bindings

    def _radioButtonCriteria(self, collection, arg=None):
        """Returns the MatchCriteria to be used for locating radio buttons
        by collection.

        Arguments:
        - collection: the collection interface for the document
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        role = [pyatspi.ROLE_RADIO_BUTTON]
        state = [pyatspi.STATE_FOCUSABLE, pyatspi.STATE_SENSITIVE]
        stateMatch = collection.MATCH_ALL
        return MatchCriteria(collection,
                             states=state,
                             matchStates=stateMatch,
                             roles=role)

    def _radioButtonPredicate(self, obj, arg=None):
        """The predicate to be used for verifying that the object
        obj is a radio button.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        isMatch = False
        if obj and obj.getRole() == pyatspi.ROLE_RADIO_BUTTON:
            state = obj.getState()
            isMatch = state.contains(pyatspi.STATE_FOCUSABLE) \
                and state.contains(pyatspi.STATE_SENSITIVE)

        return isMatch

    def _radioButtonPresentation(self, obj, arg=None):
        """Presents the radio button or indicates that one was not found.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        if obj:
            obj.queryComponent().grabFocus()
        else:
            full = messages.NO_MORE_RADIO_BUTTONS
            brief = messages.STRUCTURAL_NAVIGATION_NOT_FOUND
            self._script.presentMessage(full, brief)

    def _radioButtonDialogData(self):
        columnHeaders = [guilabels.SN_HEADER_RADIO_BUTTON]
        columnHeaders.append(guilabels.SN_HEADER_STATE)

        def rowData(obj):
            return [self._getLabel(obj), self._getState(obj)]

        return guilabels.SN_TITLE_RADIO_BUTTON, columnHeaders, rowData
    #
    #
    # Separators           #
    #
    #

    def _separatorBindings(self):
        """Returns a dictionary of [keysymstring, modifiers, description]
        lists for navigating amongst separators.
        """

        bindings = {}
        prevDesc = cmdnames.SEPARATOR_PREV
        bindings["previous"] = ["s", settings.SHIFT_MODIFIER_MASK, prevDesc]

        nextDesc = cmdnames.SEPARATOR_NEXT
        bindings["next"] = ["s", settings.NO_MODIFIER_MASK, nextDesc]
        return bindings

    def _separatorCriteria(self, collection, arg=None):
        """Returns the MatchCriteria to be used for locating separators
        by collection.

        Arguments:
        - collection: the collection interface for the document
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        role = [pyatspi.ROLE_SEPARATOR]
        return MatchCriteria(collection, roles=role, applyPredicate=False)

    def _separatorPredicate(self, obj, arg=None):
        """The predicate to be used for verifying that the object
        obj is a separator.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        return obj and obj.getRole() == pyatspi.ROLE_SEPARATOR

    def _separatorPresentation(self, obj, arg=None):
        """Presents the separator or indicates that one was not found.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        if obj:
            [newObj, characterOffset] = self._getCaretPosition(obj)
            self._setCaretPosition(newObj, characterOffset)
            self._presentObject(obj, 0)
        else:
            full = messages.NO_MORE_SEPARATORS
            brief = messages.STRUCTURAL_NAVIGATION_NOT_FOUND
            self._script.presentMessage(full, brief)
    #
    #
    # Tables               #
    #
    #

    def _tableBindings(self):
        """Returns a dictionary of [keysymstring, modifiers, description]
        lists for navigating amongst tables.
        """

        bindings = {}
        prevDesc = cmdnames.TABLE_PREV
        bindings["previous"] = ["t", settings.SHIFT_MODIFIER_MASK, prevDesc]

        nextDesc = cmdnames.TABLE_NEXT
        bindings["next"] = ["t", settings.NO_MODIFIER_MASK, nextDesc]

        listDesc = cmdnames.TABLE_LIST
        bindings["list"] = ["t", settings.SHIFT_ALT_MODIFIER_MASK, listDesc]
        return bindings

    def _tableCriteria(self, collection, arg=None):
        """Returns the MatchCriteria to be used for locating tables
        by collection.

        Arguments:
        - collection: the collection interface for the document
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        role = [pyatspi.ROLE_TABLE]
        return MatchCriteria(collection, roles=role, applyPredicate=True)

    def _tablePredicate(self, obj, arg=None):
        """The predicate to be used for verifying that the object
        obj is a table.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        if obj and obj.childCount and obj.getRole() == pyatspi.ROLE_TABLE:
            try:
                return obj.queryTable().nRows > 0
            except:
                pass

        return False

    def _tablePresentation(self, obj, arg=None):
        """Presents the table or indicates that one was not found.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        if obj:
            caption = self._getTableCaption(obj)
            if caption:
                self._script.presentMessage(caption)
            self._script.presentMessage(self._getTableDescription(obj))
            cell = obj.queryTable().getAccessibleAt(0, 0)
            self.lastTableCell = [0, 0]
            [cell, characterOffset] = self._getCaretPosition(cell)
            self._setCaretPosition(cell, characterOffset)
            self._presentObject(cell, characterOffset)
        else:
            full = messages.NO_MORE_TABLES
            brief = messages.STRUCTURAL_NAVIGATION_NOT_FOUND
            self._script.presentMessage(full, brief)

    def _tableDialogData(self):
        columnHeaders = [guilabels.SN_HEADER_CAPTION]
        columnHeaders.append(guilabels.SN_HEADER_DESCRIPTION)

        def rowData(obj):
            return [self._getTableCaption(obj) or '',
                    self._getTableDescription(obj)]

        return guilabels.SN_TITLE_TABLE, columnHeaders, rowData
    #
    #
    # Table Cells          #
    #
    #

    def _tableCellBindings(self):
        """Returns a dictionary of [keysymstring, modifiers, description]
        lists for navigating spatially amongst table cells.
        """

        bindings = {}
        desc = cmdnames.TABLE_CELL_LEFT
        bindings["left"] = ["Left", settings.SHIFT_ALT_MODIFIER_MASK, desc]

        desc = cmdnames.TABLE_CELL_RIGHT
        bindings["right"] = ["Right", settings.SHIFT_ALT_MODIFIER_MASK, desc]

        desc = cmdnames.TABLE_CELL_UP
        bindings["up"] = ["Up", settings.SHIFT_ALT_MODIFIER_MASK, desc]

        desc = cmdnames.TABLE_CELL_DOWN
        bindings["down"] = ["Down", settings.SHIFT_ALT_MODIFIER_MASK, desc]

        desc = cmdnames.TABLE_CELL_FIRST
        bindings["first"] = ["Home", settings.SHIFT_ALT_MODIFIER_MASK, desc]

        desc = cmdnames.TABLE_CELL_LAST
        bindings["last"] = ["End", settings.SHIFT_ALT_MODIFIER_MASK, desc]
        return bindings

    def _tableCellCriteria(self, collection, arg=None):
        """Returns the MatchCriteria to be used for locating table cells
        by collection.

        Arguments:
        - collection: the collection interface for the document
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        role = [pyatspi.ROLE_TABLE_CELL,
                pyatspi.ROLE_COLUMN_HEADER,
                pyatspi.ROLE_ROW_HEADER]
        return MatchCriteria(collection, roles=role)

    def _tableCellPredicate(self, obj, arg=None):
        """The predicate to be used for verifying that the object
        obj is a table cell.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        return (obj and obj.getRole() in [pyatspi.ROLE_COLUMN_HEADER,
                                          pyatspi.ROLE_ROW_HEADER,
                                          pyatspi.ROLE_TABLE_CELL])

    def _tableCellPresentation(self, cell, arg):
        """Presents the table cell or indicates that one was not found.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        if not cell:
            return

        if settings.speakCellHeaders:
            self._presentCellHeaders(cell, arg)

        [obj, characterOffset] = self._getCaretPosition(cell)
        self._setCaretPosition(obj, characterOffset)
        self._script.updateBraille(obj)

        blank = self._isBlankCell(cell)
        if not blank:
            self._presentObject(cell, 0)
        else:
            speech.speak(messages.BLANK)

        if settings.speakCellCoordinates:
            [row, col] = self.getCellCoordinates(cell)
            self._script.presentMessage(messages.TABLE_CELL_COORDINATES
                                        % {"row": row + 1, "column": col + 1})

        spanString = self._getCellSpanInfo(cell)
        if spanString and settings.speakCellSpan:
            self._script.presentMessage(spanString)
    #
    #
    # Unvisited Links      #
    #
    #

    def _unvisitedLinkBindings(self):
        """Returns a dictionary of [keysymstring, modifiers, description]
        lists for navigating amongst unvisited links.
        """

        bindings = {}
        prevDesc = cmdnames.UNVISITED_LINK_PREV
        bindings["previous"] = ["u", settings.SHIFT_MODIFIER_MASK, prevDesc]

        nextDesc = cmdnames.UNVISITED_LINK_NEXT
        bindings["next"] = ["u", settings.NO_MODIFIER_MASK, nextDesc]

        listDesc = cmdnames.UNVISITED_LINK_LIST
        bindings["list"] = ["u", settings.SHIFT_ALT_MODIFIER_MASK, listDesc]

        return bindings

    def _unvisitedLinkCriteria(self, collection, arg=None):
        """Returns the MatchCriteria to be used for locating unvisited links
        by collection.

        Arguments:
        - collection: the collection interface for the document
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        role = [pyatspi.ROLE_LINK]
        state = [pyatspi.STATE_VISITED]
        stateMatch = collection.MATCH_NONE
        return MatchCriteria(collection,
                             states=state,
                             matchStates=stateMatch,
                             roles=role,
                             applyPredicate=True)

    def _unvisitedLinkPredicate(self, obj, arg=None):
        """The predicate to be used for verifying that the object
        obj is an unvisited link.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        isMatch = False

        if obj and obj.getRole() == pyatspi.ROLE_LINK:
            state = obj.getState()
            isMatch = not state.contains(pyatspi.STATE_VISITED) \
                and state.contains(pyatspi.STATE_FOCUSABLE)

        return isMatch

    def _unvisitedLinkPresentation(self, obj, arg=None):
        """Presents the unvisited link or indicates that one was not
        found.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        if obj:
            # We were counting on the Gecko script's setCaretPosition
            # to do the focus grab. It turns out that we do not always
            # want setCaretPosition to grab focus on a link (e.g. when
            # arrowing in the text of a paragraph which is a child of
            # a link. Therefore, we need to grab focus here.
            #
            obj.queryComponent().grabFocus()
        else:
            full = messages.NO_MORE_UNVISITED_LINKS
            brief = messages.STRUCTURAL_NAVIGATION_NOT_FOUND
            self._script.presentMessage(full, brief)

    def _unvisitedLinkDialogData(self):
        columnHeaders = [guilabels.SN_HEADER_LINK]
        columnHeaders.append(guilabels.SN_HEADER_URI)

        def rowData(obj):
            return [self._getText(obj), self._script.utilities.uri(obj)]

        return guilabels.SN_TITLE_UNVISITED_LINK, columnHeaders, rowData
    #
    #
    # Visited Links        #
    #
    #

    def _visitedLinkBindings(self):
        """Returns a dictionary of [keysymstring, modifiers, description]
        lists for navigating amongst visited links.
        """

        bindings = {}
        prevDesc = cmdnames.VISITED_LINK_PREV
        bindings["previous"] = ["v", settings.SHIFT_MODIFIER_MASK, prevDesc]

        nextDesc = cmdnames.VISITED_LINK_NEXT
        bindings["next"] = ["v", settings.NO_MODIFIER_MASK, nextDesc]

        listDesc = cmdnames.VISITED_LINK_LIST
        bindings["list"] = ["v", settings.SHIFT_ALT_MODIFIER_MASK, listDesc]

        return bindings

    def _visitedLinkCriteria(self, collection, arg=None):
        """Returns the MatchCriteria to be used for locating visited links
        by collection.

        Arguments:
        - collection: the collection interface for the document
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        role = [pyatspi.ROLE_LINK]
        state = [pyatspi.STATE_VISITED, pyatspi.STATE_FOCUSABLE]
        stateMatch = collection.MATCH_ALL
        return MatchCriteria(collection,
                             states=state,
                             matchStates=stateMatch,
                             roles=role)

    def _visitedLinkPredicate(self, obj, arg=None):
        """The predicate to be used for verifying that the object
        obj is a visited link.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        isMatch = False

        if obj and obj.getRole() == pyatspi.ROLE_LINK:
            state = obj.getState()
            isMatch = state.contains(pyatspi.STATE_VISITED) \
                and state.contains(pyatspi.STATE_FOCUSABLE)

        return isMatch

    def _visitedLinkPresentation(self, obj, arg=None):
        """Presents the visited link or indicates that one was not
        found.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """
        if obj:
            obj.queryComponent().grabFocus()
        else:
            full = messages.NO_MORE_VISITED_LINKS
            brief = messages.STRUCTURAL_NAVIGATION_NOT_FOUND
            self._script.presentMessage(full, brief)

    def _visitedLinkDialogData(self):
        columnHeaders = [guilabels.SN_HEADER_LINK]
        columnHeaders.append(guilabels.SN_HEADER_URI)

        def rowData(obj):
            return [self._getText(obj), self._script.utilities.uri(obj)]

        return guilabels.SN_TITLE_VISITED_LINK, columnHeaders, rowData
    #
    #
    # Plain ol' Links      #
    #
    #

    def _linkBindings(self):
        """Returns a dictionary of [keysymstring, modifiers, description]
        lists for navigating amongst links.
        """

        bindings = {}
        listDesc = cmdnames.LINK_LIST
        bindings["list"] = ["k", settings.SHIFT_ALT_MODIFIER_MASK, listDesc]
        return bindings

    def _linkCriteria(self, collection, arg=None):
        """Returns the MatchCriteria to be used for locating unvisited links
        by collection.

        Arguments:
        - collection: the collection interface for the document
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        role = [pyatspi.ROLE_LINK]
        state = [pyatspi.STATE_FOCUSABLE]
        stateMatch = collection.MATCH_ALL
        return MatchCriteria(collection,
                             states=state,
                             matchStates=stateMatch,
                             roles=role)

    def _linkPredicate(self, obj, arg=None):
        """The predicate to be used for verifying that the object
        obj is an link.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        isMatch = False
        if obj and obj.getRole() == pyatspi.ROLE_LINK:
            state = obj.getState()
            isMatch = not state.contains(pyatspi.STATE_FOCUSABLE)
        return isMatch

    def _linkPresentation(self, obj, arg=None):
        """Presents the link or indicates that one was not found.

        Arguments:
        - obj: the accessible object under consideration.
        - arg: an optional argument which may need to be included in
          the criteria (e.g. the level of a heading).
        """

        if obj:
            # We were counting on the Gecko script's setCaretPosition
            # to do the focus grab. It turns out that we do not always
            # want setCaretPosition to grab focus on a link (e.g. when
            # arrowing in the text of a paragraph which is a child of
            # a link. Therefore, we need to grab focus here.
            #
            obj.queryComponent().grabFocus()
        else:
            full = messages.NO_MORE_LINKS
            brief = messages.STRUCTURAL_NAVIGATION_NOT_FOUND
            self._script.presentMessage(full, brief)

    def _linkDialogData(self):
        columnHeaders = [guilabels.SN_HEADER_LINK]
        columnHeaders.append(guilabels.SN_HEADER_STATE)
        columnHeaders.append(guilabels.SN_HEADER_URI)

        def rowData(obj):
            return [self._getText(obj),
                    self._getState(obj),
                    self._script.utilities.uri(obj)]

        return guilabels.SN_TITLE_LINK, columnHeaders, rowData
