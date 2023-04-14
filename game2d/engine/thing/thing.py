#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Abstract thing class.
"""

from .. import figure

__version__ = (0, 0, 3, 1)


class g2dThing(figure.g2dFigure):
    """
    Abstract thing class.
    """
    def __init__(self, scene):
        """
        Constructor.
        :param scene: Scene object.
        """
        figure.g2dFigure.__init__(self, scene)

