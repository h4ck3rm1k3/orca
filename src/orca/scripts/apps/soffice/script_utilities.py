# Orca
#
# Copyright 2010 Joanmarie Diggs.
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

"""Commonly-required utility methods needed by -- and potentially
   customized by -- application and toolkit scripts. They have
   been pulled out from the scripts because certain scripts had
   gotten way too large as a result of including these methods."""

__id__ = "$Id$"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2010 Joanmarie Diggs."
__license__ = "LGPL"

import pyatspi

import orca.debug as debug
import orca.orca_state as orca_state
import orca.script_utilities as script_utilities

#
#
# Utilities                                                                 #
#
#


class Utilities(script_utilities.Utilities):

    def __init__(self, script):
        """Creates an instance of the Utilities class.

        Arguments:
        - script: the script with which this instance is associated.
        """

        script_utilities.Utilities.__init__(self, script)

    #
    #
    # Utilities for finding, identifying, and comparing accessibles         #
    #
    #

    def displayedText(self, obj):
        """Returns the text being displayed for an object. Overridden here
        because OpenOffice uses symbols (e.g. ">>" for buttons but exposes
        more useful information via the accessible's name.

        Arguments:
        - obj: the object

        Returns the text being displayed for an object or None if there isn't
        any text being shown.
        """

        role = obj.getRole()
        if role == pyatspi.ROLE_PUSH_BUTTON and obj.name:
            return obj.name

        if role == pyatspi.ROLE_TABLE_CELL:
            strings = list(map(self.displayedText, [child for child in obj]))
            text = "\n".join(strings)
            if text.strip():
                return text

        return script_utilities.Utilities.displayedText(self, obj)

    def isReadOnlyTextArea(self, obj):
        """Returns True if obj is a text entry area that is read only."""

        if not obj.getRole() == pyatspi.ROLE_TEXT:
            return False

        state = obj.getState()
        readOnly = state.contains(pyatspi.STATE_FOCUSABLE) \
            and not state.contains(pyatspi.STATE_EDITABLE)
        details = debug.getAccessibleDetails(debug.LEVEL_ALL, obj)
        debug.println(debug.LEVEL_ALL,
                      "soffice - isReadOnlyTextArea=%s for %s" %
                      (readOnly, details))

        return readOnly

    def isCellBeingEdited(self, obj):
        if not obj:
            return False

        parent = obj.parent
        if parent and parent.getRoleName() == 'text frame':
            if self.spreadSheetCellName(parent):
                return True

        return False

    def isSpreadSheetCell(self, obj, startFromTable=False):
        """Return an indication of whether the given obj is a spread sheet
        table cell.

        Arguments:
        - obj: the object to check.
        - startFromTable: if True, then the component hierarchy check should
          start from a table (as opposed to a table cell).

        Returns True if this is a table cell, False otherwise.
        """

        cell = obj
        if not startFromTable:
            obj = obj.parent

        try:
            table = obj.queryTable()
        except:
            return self.isCellBeingEdited(cell)
        else:
            return table.nRows in [65536, 1048576]

    def isDocumentCell(self, cell):
        isCell = lambda x: x and x.getRole() == pyatspi.ROLE_TABLE_CELL
        if not isCell(cell):
            cell = pyatspi.findAncestor(cell, isCell)

        if not cell or self.isSpreadSheetCell(cell):
            return False

        isDocument = lambda x: x and x.getRole() == pyatspi.ROLE_DOCUMENT_FRAME
        return pyatspi.findAncestor(cell, isDocument) != None

    def spreadSheetCellName(self, cell):
        nameList = cell.name.split()
        for name in nameList:
            if not name.isalpha() and name.isalnum():
                return name

        return ''

    def getRowColumnAndTable(self, cell):
        """Returns the (row, column, table) tuple for cell."""

        if not (cell and cell.getRole() == pyatspi.ROLE_TABLE_CELL):
            return -1, -1, None

        cellParent = cell.parent
        if cellParent and cellParent.getRole() == pyatspi.ROLE_TABLE_CELL:
            cell = cellParent
            cellParent = cell.parent

        table = cellParent
        if table and table.getRole() != pyatspi.ROLE_TABLE:
            table = table.parent

        try:
            iTable = table.queryTable()
        except:
            return -1, -1, None

        index = self.cellIndex(cell)
        row = iTable.getRowAtIndex(index)
        column = iTable.getColumnAtIndex(index)

        return row, column, table

    def getShowingCellsInRow(self, obj):
        row, column, parentTable = self.getRowColumnAndTable(obj)
        try:
            table = parentTable.queryTable()
        except:
            return []

        startIndex, endIndex = self.getTableRowRange(obj)
        cells = []
        for i in range(startIndex, endIndex):
            cell = table.getAccessibleAt(row, i)
            try:
                showing = cell.getState().contains(pyatspi.STATE_SHOWING)
            except:
                continue
            if showing:
                cells.append(cell)

        return cells

    def getTableRowRange(self, obj):
        """If this is spread sheet cell, return the start and end indices
        of the spread sheet cells for the table that obj is in. Otherwise
        return the complete range (0, parentTable.nColumns).

        Arguments:
        - obj: a table cell.

        Returns the start and end table cell indices.
        """

        parent = obj.parent
        try:
            parentTable = parent.queryTable()
        except NotImplementedError:
            parentTable = None

        startIndex = 0
        endIndex = parentTable.nColumns

        if self.isSpreadSheetCell(obj):
            extents = parent.queryComponent().getExtents(
                pyatspi.DESKTOP_COORDS)
            y = extents.y
            leftX = extents.x + 1
            leftCell = \
                parent.queryComponent().getAccessibleAtPoint(leftX, y, 0)
            if leftCell:
                table = leftCell.parent.queryTable()
                index = self.cellIndex(leftCell)
                startIndex = table.getColumnAtIndex(index)

            rightX = extents.x + extents.width - 1
            rightCell = \
                parent.queryComponent().getAccessibleAtPoint(rightX, y, 0)
            if rightCell:
                table = rightCell.parent.queryTable()
                index = self.cellIndex(rightCell)
                endIndex = table.getColumnAtIndex(index) + 1

        return [startIndex, endIndex]

    def getDynamicHeadersForCell(self, obj, onlyIfNew=False):
        if not (self._script.dynamicRowHeaders or self._script.dynamicColumnHeaders):
            return None, None

        objRow, objCol, table = self.getRowColumnAndTable(obj)
        if not table:
            return None, None

        headersRow = self._script.dynamicColumnHeaders.get(hash(table))
        headersCol = self._script.dynamicRowHeaders.get(hash(table))
        if headersRow == objRow or headersCol == objCol:
            return None, None

        getRowHeader = headersCol != None
        getColHeader = headersRow != None
        if onlyIfNew:
            getRowHeader = \
                getRowHeader and objRow != \
                self._script.pointOfReference.get(
                    "lastRow")
            getColHeader = \
                getColHeader and objCol != \
                self._script.pointOfReference.get(
                    "lastColumn")

        parentTable = table.queryTable()
        rowHeader, colHeader = None, None
        if getColHeader:
            colHeader = parentTable.getAccessibleAt(headersRow, objCol)

        if getRowHeader:
            rowHeader = parentTable.getAccessibleAt(objRow, headersCol)

        return rowHeader, colHeader

    def isSameObject(self, obj1, obj2):
        same = script_utilities.Utilities.isSameObject(self, obj1, obj2)

        # Handle the case of false positives in dialog boxes resulting
        # from getIndexInParent() returning a bogus value. bgo#618790.
        #
        if same and (obj1 != obj2) and not obj1.name \
           and obj1.getRole() == pyatspi.ROLE_TABLE_CELL \
           and obj1.getIndexInParent() == obj2.getIndexInParent() == -1:
            top = self.topLevelObject(obj1)
            if top and top.getRole() == pyatspi.ROLE_DIALOG:
                same = False

        return same

    def isLayoutOnly(self, obj):
        """Returns True if the given object is a container which has
        no presentable information (label, name, displayed text, etc.)."""

        role = obj.getRole()
        if role == pyatspi.ROLE_PANEL and obj.childCount == 1:
            if obj.name and obj.name == obj[0].name:
                return True

        if role == pyatspi.ROLE_LIST \
           and obj.parent.getRole() == pyatspi.ROLE_COMBO_BOX:
            return True

        return script_utilities.Utilities.isLayoutOnly(self, obj)

    def locateInputLine(self, obj):
        """Return the spread sheet input line. This only needs to be found
        the very first time a spread sheet table cell gets focus. We use the
        table cell to work back up the component hierarchy until we have found
        the common panel that both it and the input line reside in. We then
        use that as the base component to search for a component which has a
        paragraph role. This will be the input line.

        Arguments:
        - obj: the spread sheet table cell that has just got focus.

        Returns the spread sheet input line component.
        """

        if self._script.inputLineForCell:
            return self._script.inputLineForCell

        isScrollPane = lambda x: x and x.getRole() == pyatspi.ROLE_SCROLL_PANE
        scrollPane = pyatspi.findAncestor(obj, isScrollPane)
        if not scrollPane:
            return None

        toolbar = None
        for child in scrollPane.parent:
            if child and child.getRole() == pyatspi.ROLE_TOOL_BAR:
                toolbar = child
                break

        isParagraph = lambda x: x and x.getRole() == pyatspi.ROLE_PARAGRAPH
        allParagraphs = pyatspi.findAllDescendants(toolbar, isParagraph)
        if len(allParagraphs) == 1:
            self._script.inputLineForCell = allParagraphs[0]

        return self._script.inputLineForCell

    def frameAndDialog(self, obj):
        """Returns the frame and (possibly) the dialog containing
        the object. Overridden here for presentation of the title
        bar information: If the locusOfFocus is a spreadsheet cell,
        1) we are not in a dialog and 2) we need to present both the
        frame name and the sheet name. So we might as well return the
        sheet in place of the dialog so that the default code can do
        its thing.
        """

        if not self.isSpreadSheetCell(obj):
            return script_utilities.Utilities.frameAndDialog(self, obj)

        results = [None, None]

        parent = obj.parent
        while parent and (parent.parent != parent):
            if parent.getRole() == pyatspi.ROLE_FRAME:
                results[0] = parent
            if parent.getRole() == pyatspi.ROLE_TABLE:
                results[1] = parent
            parent = parent.parent

        return results

    def isFunctionalDialog(self, obj):
        """Returns true if the window is functioning as a dialog."""

        # The OOo Navigator window looks like a dialog, acts like a
        # dialog, and loses focus requiring the user to know that it's
        # there and needs Alt+F6ing into.  But officially it's a normal
        # window.

        # There doesn't seem to be (an efficient) top-down equivalent
        # of utilities.hasMatchingHierarchy(). But OOo documents have
        # root panes; this thing does not.
        #
        rolesList = [pyatspi.ROLE_FRAME,
                     pyatspi.ROLE_PANEL,
                     pyatspi.ROLE_PANEL,
                     pyatspi.ROLE_TOOL_BAR,
                     pyatspi.ROLE_PUSH_BUTTON]

        if obj.getRole() != rolesList[0]:
            # We might be looking at the child.
            #
            rolesList.pop(0)

        while obj and obj.childCount and len(rolesList):
            if obj.getRole() != rolesList.pop(0):
                return False
            obj = obj[0]

        return True

    def validParent(self, obj):
        """Returns the first valid parent/ancestor of obj. We need to do
        this in some applications and toolkits due to bogus hierarchies.

        See bugs:
        http://www.openoffice.org/issues/show_bug.cgi?id=78117
        http://bugzilla.gnome.org/show_bug.cgi?id=489490

        Arguments:
        - obj: the Accessible object
        """

        parent = obj.parent
        if parent and parent.getRole() in (pyatspi.ROLE_ROOT_PANE,
                                           pyatspi.ROLE_DIALOG):
            app = obj.getApplication()
            for frame in app:
                if frame.childCount < 1 \
                   or frame[0].getRole() not in (pyatspi.ROLE_ROOT_PANE,
                                                 pyatspi.ROLE_OPTION_PANE):
                    continue

                root_pane = frame[0]
                if obj in root_pane:
                    return root_pane

        return parent

    def findPreviousObject(self, obj):
        """Finds the object before this one."""

        if not obj:
            return None

        for relation in obj.getRelationSet():
            if relation.getRelationType() == pyatspi.RELATION_FLOWS_FROM:
                return relation.getTarget(0)

        index = obj.getIndexInParent() - 1
        if not (0 <= index < obj.parent.childCount - 1):
            obj = obj.parent
            index = obj.getIndexInParent() - 1

        try:
            prevObj = obj.parent[index]
        except:
            prevObj = obj

        return prevObj

    def findNextObject(self, obj):
        """Finds the object after this one."""

        if not obj:
            return None

        for relation in obj.getRelationSet():
            if relation.getRelationType() == pyatspi.RELATION_FLOWS_TO:
                return relation.getTarget(0)

        index = obj.getIndexInParent() + 1
        if not (0 < index < obj.parent.childCount):
            obj = obj.parent
            index = obj.getIndexInParent() + 1

        try:
            nextObj = obj.parent[index]
        except:
            nextObj = None

        return nextObj

    #
    #
    # Impress-Specific Utilities                                            #
    #
    #

    def drawingView(self, obj=orca_state.locusOfFocus):
        """Attempts to locate the Impress drawing view, which is the
        area in which slide editing occurs."""

        # TODO - JD: We should probably add this to the generatorCache.
        #
        docFrames = self.descendantsWithRole(
            self.topLevelObject(obj), pyatspi.ROLE_DOCUMENT_FRAME)
        docFrame = [o for o in docFrames if ":" in o.name and "/" in o.name]
        if docFrame:
            return docFrame[0]

        return None

    def isDrawingView(self, obj):
        """Returns True if obj is the Impress Drawing View."""

        if obj and obj.getRole() == pyatspi.ROLE_DOCUMENT_FRAME:
            return (":" in obj.name and "/" in obj.name)

        return False

    def isInImpress(self, obj=orca_state.locusOfFocus):
        """Returns True if obj is in OOo Impress."""

        # Having checked English, Spanish, and Arabic, it would seem
        # that the Frame name will end with "Impress", unlocalized.
        #
        if obj:
            topLevel = self.topLevelObject(obj)
            if topLevel and topLevel.name.endswith("Impress"):
                return True

        return False

    def slideAndTaskPanes(self, obj=orca_state.locusOfFocus):
        """Attempts to locate the Impress slide pane and task pane."""

        drawingView = self.drawingView(obj)
        if not drawingView:
            return None, None

        parent = drawingView.parent
        if parent:
            parent = parent.parent
        if not parent:
            return None, None

        panes = self.descendantsWithRole(parent, pyatspi.ROLE_SPLIT_PANE)
        if not panes:
            return None, None

        slidePane = taskPane = None
        if self.descendantsWithRole(panes[0], pyatspi.ROLE_DOCUMENT_FRAME):
            slidePane = panes[0]
            if len(panes) == 2:
                taskPane = panes[1]
        else:
            taskPane = panes[0]
            if len(panes) == 2:
                slidePane = panes[1]

        return slidePane, taskPane

    def slideTitleAndPosition(self, obj):
        """Attempts to obtain the title, position of the slide which contains
        or is represented by obj.

        Returns a (title, position, count) tuple.
        """

        if obj.getRole() == pyatspi.ROLE_DOCUMENT_FRAME:
            dv = obj
        else:
            dv = self.ancestorWithRole(obj, [pyatspi.ROLE_DOCUMENT_FRAME], [])

        if not dv or not self.isDrawingView(dv):
            return "", 0, 0

        positionAndCount = dv.name.split(":")[1]
        position, count = positionAndCount.split("/")
        title = ""
        for child in dv:
            if not child.childCount:
                continue
            # We want an actual Title.
            #
            if child.name.startswith("ImpressTitle"):
                title = self.displayedText(child[0])
                break
            # But we'll live with a Subtitle if we can't find a title.
            # Unlike Titles, a single subtitle can be made up of multiple
            # accessibles.
            #
            elif child.name.startswith("ImpressSubtitle"):
                for line in child:
                    title = self.appendString(title, self.displayedText(line))

        return title, int(position), int(count)

    #
    #
    # Utilities for working with the accessible text interface              #
    #
    #

    def isWordMisspelled(self, obj, offset):
        """Identifies if the current word is flagged as misspelled by the
        application.

        Arguments:
        - obj: An accessible which implements the accessible text interface.
        - offset: Offset in the accessible's text for which to retrieve the
          attributes.

        Returns True if the word is flagged as misspelled.
        """

        attributes, start, end = self.textAttributes(obj, offset, True)
        error = attributes.get("text-spelling")

        return error == "misspelled"

    def substring(self, obj, startOffset, endOffset):
        """Returns the substring of the given object's text specialization.

        NOTE: This is here to handle the problematic implementation of
        getText by OpenOffice.  See the bug discussion at:

           http://bugzilla.gnome.org/show_bug.cgi?id=356425)

        Once the OpenOffice issue has been resolved, this method probably
        should be removed.

        Arguments:
        - obj: an accessible supporting the accessible text specialization
        - startOffset: the starting character position
        - endOffset: the ending character position
        """

        text = obj.queryText().getText(0, -1)
        if startOffset >= len(text):
            startOffset = len(text) - 1
        if endOffset == -1:
            endOffset = len(text)
        elif startOffset >= endOffset:
            endOffset = startOffset + 1
        string = text[max(0, startOffset):min(len(text), endOffset)]

        return string

    def textAttributes(self, acc, offset, get_defaults=False):
        """Get the text attributes run for a given offset in a given accessible

        Arguments:
        - acc: An accessible.
        - offset: Offset in the accessible's text for which to retrieve the
        attributes.
        - get_defaults: Get the default attributes as well as the unique ones.
        Default is True

        Returns a dictionary of attributes, a start offset where the attributes
        begin, and an end offset. Returns ({}, 0, 0) if the accessible does not
        supprt the text attribute.
        """
        rv, start, end = script_utilities.Utilities.\
            textAttributes(self, acc, offset, get_defaults)

        # If there are no text attributes associated with the text at a
        # given offset, we might get some seriously bogus offsets, in
        # particular, an extremely large start offset and an extremely
        # large, but negative end offset. As a result, any text attributes
        # which are present on the line after the specified offset will
        # not be indicated by braille.py's getAttributeMask. Therefore,
        # we'll set the start offset to the character being examined,
        # and the end offset to the next character.
        #
        start = min(start, offset)
        if end < 0:
            debug.println(debug.LEVEL_WARNING,
                          "soffice.script.py:getTextAttributes: detected a bogus " +
                          "end offset. Start offset: %s, end offset: %s" % (start, end))
            end = offset + 1

        return rv, start, end

    #
    #
    # Miscellaneous Utilities                                               #
    #
    #

    def isAutoTextEvent(self, event):
        """Returns True if event is associated with text being autocompleted
        or autoinserted or autocorrected or autosomethingelsed.

        Arguments:
        - event: the accessible event being examined
        """

        if event.source.getRole() != pyatspi.ROLE_PARAGRAPH:
            return False

        lastKey, mods = self.lastKeyAndModifiers()
        if event.type.startswith("object:text-changed:insert"):
            if not event.any_data:
                return False

            if lastKey == "Tab" and event.any_data != "\t":
                return True

            if lastKey in ["BackSpace", "ISO_Left_Tab"]:
                return True

        if event.type.startswith("focus:"):
            if lastKey == "Return":
                try:
                    charCount = event.source.queryText().characterCount
                except:
                    charCount = 0
                return charCount > 0

        return False

    def selectedChildren(self, obj):
        if not obj:
            return []

        # Things only seem broken for certain tables, e.g. the Paths table.
        # TODO - JD: File the LibreOffice bugs and reference them here.
        if obj.getRole() != pyatspi.ROLE_TABLE \
           or self.isSpreadSheetCell(obj, True):
            return script_utilities.Utilities.selectedChildren(self, obj)

        try:
            selection = obj.querySelection()
        except:
            return []

        children = []
        for i, child in enumerate(obj):
            if selection.isChildSelected(i):
                children.append(obj[i])

        return children
