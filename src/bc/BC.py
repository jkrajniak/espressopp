from espresso import pmi
from espresso import toReal3D, toReal3DFromVector, toInt3D, toInt3DFromVector
from _espresso import bc_BC 

class BCLocal(object):
    """Abstract local base classs for boundary conditions."""
    def getMinimumImageVector(self, pos1, pos2):
        return self.cxxclass.getMinimumImageVector(
            self, toReal3DFromVector(pos1), toReal3DFromVector(pos2))

    def getFoldedPosition(self, pos, imageBox=None):
        if imageBox is None:
            return self.cxxclass.getFoldedPosition(self, toReal3DFromVector(pos))
        else:
            return self.cxxclass.getFoldedPosition(
                self, toReal3DFromVector(pos), toInt3DFromVector(imageBox))

    def getUnfoldedPosition(self, pos, imageBox):
        return self.cxxclass.getUnfoldedPosition(
            self, toReal3DFromVector(pos), toInt3DFromVector(imageBox))

    def getRandomPos(self):
        return self.cxxclass.getRandomPos(self)

if pmi.isController :
    class BC(object):
        """Abstract base classs for boundary conditions."""
        __metaclass__ = pmi.Proxy
        pmiproxydefs = dict(
            pmiproperty = [ "boxL", "rng" ],
            localcall = [ "getMinimumImageVector", 
                          "getFoldedPosition", "getUnfoldedPosition", 
                          "getRandomPos" ]
            )