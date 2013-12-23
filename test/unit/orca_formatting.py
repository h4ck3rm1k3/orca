from orca.formatting.braille.animation import AnimationBrailleAction

class Context ():

    def asString(self, content, delimiter=" "):
        #orca/braille_generator.py
        pass 

    @property
    def obj (self):
        pass

    @property
    def label (self):
        return []

    @property
    def displayedText (self):
        return []

    @property
    def roleName (self):
        return []

    @property
    def description (self):
        return []

    def space (self, value):
        return []

c = Context()
x = AnimationBrailleAction()

p = x.unfocused(c)
print(p)
