from orca.formatting import Formatting

class Braille (Formatting):
    def __init__(self, enum):
        Formatting.__init__(self, "braille", enum)
