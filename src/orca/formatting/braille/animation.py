from orca.formatting.braille import Braille
import pyatspi
from orca.braille import Component

class AnimationBrailleAction(Braille):
    def __init__(self):
        Braille.__init__(self, pyatspi.ROLE_ANIMATION)
        
    def unfocused(self, c):
        return [
            Component(c.obj,      
                      c.asString(
                          c.label +
                          c.displayedText +
                          c.roleName +
                          (
                              c.description
                              and
                              c.space(": ") +
                              c.description
                          )
                      )
                  )
        ]
