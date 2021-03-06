#!/usr/bin/python

"""Test of page summary
"""

from macaroon.playback import *
import utils

sequence = MacroSequence()

########################################################################
# We wait for the focus to be on the Firefox window as well as for focus
# to move to the frame.
#
sequence.append(WaitForWindowActivate(utils.firefoxFrameNames, None))

########################################################################
# Load the htmlpage.html test page.
#
sequence.append(KeyComboAction("<Control>l"))
sequence.append(WaitForFocus(acc_role=pyatspi.ROLE_ENTRY))
sequence.append(TypeAction(utils.htmlURLPrefix + "htmlpage.html"))
sequence.append(KeyComboAction("Return"))
sequence.append(WaitForDocLoad())
sequence.append(WaitForFocus("HTML test page",
                             acc_role=pyatspi.ROLE_DOCUMENT_FRAME))

########################################################################
# Move to the heading level 6
#
sequence.append(utils.StartRecordingAction())
sequence.append(TypeAction("6"))
sequence.append(PauseAction(3000))
sequence.append(utils.AssertPresentationAction(
    "Navigate to 'This is a Heading 6.'",
    ["BRAILLE LINE:  'This is a Heading 6. h6'",
     "     VISIBLE:  'This is a Heading 6. h6', cursor=1",
     "SPEECH OUTPUT: 'This is a Heading 6. heading level 6'"]))

########################################################################
# Do double-click "Where Am I" via KP_Enter. 
#
sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_Enter"))
sequence.append(KeyComboAction("KP_Enter"))
sequence.append(PauseAction(30000))
sequence.append(utils.AssertPresentationAction(
    "Where Am I for page summary info",
    ["BRAILLE LINE:  'This is a Heading 6. h6'",
     "     VISIBLE:  'This is a Heading 6. h6', cursor=1",
     "BRAILLE LINE:  'This is a Heading 6. h6'",
     "     VISIBLE:  'This is a Heading 6. h6', cursor=1",
     "SPEECH OUTPUT: 'heading level 6 This is a Heading 6.'",
     "SPEECH OUTPUT: '14 headings 3 forms 47 tables 19 unvisited links'"]))

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
