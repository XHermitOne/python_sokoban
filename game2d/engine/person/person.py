#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Abstract game personage class.
"""

# --- Imports ---
from game2d.engine import figure


# --- Classes ---
class g2dPersonage(figure.g2dFigure):
    """
    Abstract game personage class.
    """
    
    def __init__(self, scene):
        """
        Constructor.
        """
        figure.g2dFigure.__init__(self, scene)

    def RunToLeft(self):
        """
        Move personage to left.
        """        
        pass

    def RunToRight(self):
        """
        Move personage to right.
        """        
        pass

    def RunToUp(self):
        """
        Move personage to up.
        """        
        pass

    def RunToDown(self):
        """
        Move personage to down.
        """        
        pass

    def UseIt(self):
        """
        Use tool.
        """
        pass

    def DoIt(self):
        """
        Do action.
        """
        pass

    def Die(self):
        """
        Die personage.
        """
        pass

    def MoveToPoint(self, point_x, point_y):
        """
        Move personage to point (point_x, point_y).
        @param point_x, point_y: New point.
        """
        pass

    def MoveToPos(self, pos_x, pos_y):
        """
        Move personage to position (pos_x, pos_y).
        @param pos_x, pos_y: New position.
        """
        pass
