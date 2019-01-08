from .shapes import Shapes

class Board(Shapes):
    def __init__(self, magoz, light_source):
        Shapes.__init__(self, magoz, light_source, 'ex12/Main_Body_Left_Side.obj', "navy")
        self.__class__ = Board


