import numpy
from math import sin, cos, tan, pi

class Matrix(object):

    @staticmethod
    def makeIdentity():
        return numpy.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]).astype(float)
    
    @staticmethod 
    def makeTanslation(x, y, z):
        return numpy.array([
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1],
        ]).astype(float)
    
    @staticmethod
    def makeRotationX(angle):
        # x is fixed when rotating around this axis, therefore y and z
        # considered; see y/z rotation-methods, specially z which fixes the
        # z axis and rotates y, x coordinates
        c = cos(angle)
        s = sin(angle)

        return numpy.array([
            [1, 0,  0, 0],
            [0, c, -s, 0],
            [0, s,  c, 0],
            [0, 0, 0, 1]  
        ]).astype(float)
    
    
    @staticmethod
    def makeRotationY(angle):
        c = cos(angle)
        s = sin(angle)

        return numpy.array([
            [c,  0,  s, 0],
            [0,  1,  0, 0],
            [-s, 0,  c, 0],
            [0,  0,  0, 1]  
        ]).astype(float)

    @staticmethod
    def makeRotationZ(angle):
        c = cos(angle)
        s = sin(angle)

        return numpy.array([
            [c, -s, 0, 0],
            [s,  c, 0, 0],
            [0,  0, 1, 0],
            [0,  0, 0, 1]  
        ]).astype(float)
