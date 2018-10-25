#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Abstract thing class.
"""

# --- Imports ---
import game2d.engine.figure as figure

__version__ = (0, 0, 2, 1)


# --- Classes ---
class g2dThing(figure.g2dFigure):
    """
    Abstract thing class.
    """
    def __init__(self, scene):
        """
        Constructor.
        @param scene: Scene object.
        """
        figure.g2dFigure.__init__(self, scene)

