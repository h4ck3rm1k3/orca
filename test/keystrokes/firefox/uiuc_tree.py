#!/usr/bin/python

"""Test of UIUC tree presentation using Firefox.
"""

from macaroon.playback import *
import utils

sequence = MacroSequence()

########################################################################
# We wait for the focus to be on the Firefox window as well as for focus
# to move to the "inline: Tree Example 1" frame.
#
sequence.append(WaitForWindowActivate(utils.firefoxFrameNames, None))

########################################################################
# Load the UIUC button demo.
#
sequence.append(KeyComboAction("<Control>l"))
sequence.append(WaitForFocus(acc_role=pyatspi.ROLE_ENTRY))
sequence.append(TypeAction("http://test.cita.uiuc.edu/aria/tree/view_inline.php?title=Tree%20Example%201&ginc=includes/tree1_inline.inc&gcss=css/tree1_inline.css&gjs=../js/globals.js,../js/widgets_inline.js,js/tree1_inline.js"))
sequence.append(KeyComboAction("Return"))
sequence.append(WaitForDocLoad())
sequence.append(WaitForFocus("inline: Tree Example 1", acc_role=pyatspi.ROLE_DOCUMENT_FRAME))

sequence.append(PauseAction(5000))

########################################################################
# Tab to the tree.  
#
sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Tab"))
sequence.append(WaitForFocus("Fruits", acc_role=pyatspi.ROLE_LIST_ITEM))
sequence.append(utils.AssertPresentationAction(
    "tab to tree", 
    ["BRAILLE LINE:  'Fruits expanded'",
     "     VISIBLE:  'Fruits expanded', cursor=1",
     "BRAILLE LINE:  'Fruits expanded ListItem'",
     "     VISIBLE:  'Fruits expanded ListItem', cursor=1",
     "SPEECH OUTPUT: 'Foods tree'",
     "SPEECH OUTPUT: 'Fruits expanded tree level 1'"]))

########################################################################
# Do a basic "Where Am I" via KP_Enter.  
#
sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_Enter"))
sequence.append(PauseAction(3000))
sequence.append(utils.AssertPresentationAction(
    "basic whereAmI", 
    ["BRAILLE LINE:  'Fruits expanded ListItem'",
     "     VISIBLE:  'Fruits expanded ListItem', cursor=1",
     "SPEECH OUTPUT: 'list item Fruits 1 of 2 expanded tree level 1'"]))

########################################################################
# Navigate the tree using the arrows.  
#
sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Down"))
sequence.append(utils.AssertPresentationAction(
    "arrow to oranges", 
    ["BRAILLE LINE:  'Oranges ListItem'",
     "     VISIBLE:  'Oranges ListItem', cursor=1",
     "SPEECH OUTPUT: 'Oranges tree level 2'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Down"))
sequence.append(utils.AssertPresentationAction(
    "arrow to pineapples", 
    ["BRAILLE LINE:  'Pineapples ListItem'",
     "     VISIBLE:  'Pineapples ListItem', cursor=1",
     "SPEECH OUTPUT: 'Pineapples'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Down"))
sequence.append(utils.AssertPresentationAction(
    "arrow to apples", 
    ["BRAILLE LINE:  'Apples collapsed ListItem'",
     "     VISIBLE:  'Apples collapsed ListItem', cursor=1",
     "SPEECH OUTPUT: 'Apples collapsed'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Right"))
sequence.append(utils.AssertPresentationAction(
    "expand apples", 
    ["BRAILLE LINE:  'Apples expanded ListItem'",
     "     VISIBLE:  'Apples expanded ListItem', cursor=1",
     "SPEECH OUTPUT: 'expanded'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Down"))
sequence.append(utils.AssertPresentationAction(
    "arrow to macintosh", 
    ["BRAILLE LINE:  'Macintosh ListItem'",
     "     VISIBLE:  'Macintosh ListItem', cursor=1",
     "SPEECH OUTPUT: 'Macintosh tree level 3'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Down"))
sequence.append(utils.AssertPresentationAction(
    "arrow to granny smith", 
    ["BRAILLE LINE:  'Granny Smith collapsed ListItem'",
     "     VISIBLE:  'Granny Smith collapsed ListItem', cursor=1",
     "SPEECH OUTPUT: 'Granny Smith collapsed'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Right"))
sequence.append(utils.AssertPresentationAction(
    "expand granny smith", 
    ["BRAILLE LINE:  'Granny Smith expanded ListItem'",
     "     VISIBLE:  'Granny Smith expanded ListItem', cursor=1",
     "SPEECH OUTPUT: 'expanded'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Down"))
sequence.append(utils.AssertPresentationAction(
    "arrow to washington state", 
    ["BRAILLE LINE:  'Washington State ListItem'",
     "     VISIBLE:  'Washington State ListItem', cursor=1",
     "SPEECH OUTPUT: 'Washington State tree level 4'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Down"))
sequence.append(utils.AssertPresentationAction(
    "arrow to michigan", 
    ["BRAILLE LINE:  'Michigan ListItem'",
     "     VISIBLE:  'Michigan ListItem', cursor=1",
     "SPEECH OUTPUT: 'Michigan'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Down"))
sequence.append(utils.AssertPresentationAction(
    "arrow to new york", 
    ["BRAILLE LINE:  'New York ListItem'",
     "     VISIBLE:  'New York ListItem', cursor=1",
     "SPEECH OUTPUT: 'New York'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Down"))
sequence.append(utils.AssertPresentationAction(
    "arrow to fuji", 
    ["BRAILLE LINE:  'Fuji ListItem'",
     "     VISIBLE:  'Fuji ListItem', cursor=1",
     "SPEECH OUTPUT: 'Fuji tree level 3'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Down"))
sequence.append(utils.AssertPresentationAction(
    "arrow to bananas", 
    ["BRAILLE LINE:  'Bananas ListItem'",
     "     VISIBLE:  'Bananas ListItem', cursor=1",
     "SPEECH OUTPUT: 'Bananas tree level 2'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Down"))
sequence.append(utils.AssertPresentationAction(
    "arrow to pears", 
    ["BRAILLE LINE:  'Pears ListItem'",
     "     VISIBLE:  'Pears ListItem', cursor=1",
     "SPEECH OUTPUT: 'Pears'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Down"))
sequence.append(utils.AssertPresentationAction(
    "arrow to vegetables", 
    ["BRAILLE LINE:  'Vegetables expanded ListItem'",
     "     VISIBLE:  'Vegetables expanded ListItem', cursor=1",
     "SPEECH OUTPUT: 'Vegetables expanded tree level 1'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("Left"))
sequence.append(utils.AssertPresentationAction(
    "collapse vegetables", 
    ["BRAILLE LINE:  'Vegetables collapsed ListItem'",
     "     VISIBLE:  'Vegetables collapsed ListItem', cursor=1",
     "SPEECH OUTPUT: 'collapsed'"]))

########################################################################
# Close the demo
#
sequence.append(KeyComboAction("<Control>l"))
sequence.append(WaitForFocus(acc_role=pyatspi.ROLE_ENTRY))
sequence.append(TypeAction("about:blank"))
sequence.append(KeyComboAction("Return"))
sequence.append(WaitForDocLoad())
# Just a little extra wait to let some events get through.
#
sequence.append(PauseAction(3000))

sequence.append(utils.AssertionSummaryAction())

sequence.start()
