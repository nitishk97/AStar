import numpy

class cellState:
    def __init__(self, a, b, actBlockStatus: bool):
        self.loc = numpy.array([a, b])
        self.actBlockStatus = actBlockStatus
        self.discBlockStatus = False
        self.search_value = 0
        self.g_value = 0
        self.h_value = 0
        self.f_value = self.g_value + self.h_value
        self.treePtr = None

    def updateFValue(self):
        self.f_value = self.g_value + self.h_value
