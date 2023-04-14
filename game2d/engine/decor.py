#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Abstract class of decoration.
"""

# --- Imports ---
from ..tools import image as img

__version__ = (0, 0, 3, 1)


class g2dDecor:
    """
    Abstract class of decoration.
    """
    def __init__(self, scene):
        """
        Constructor.
        :param scene: Scene object.
        """
        self._Scene = scene
        self._Img = None        # Decoration image
        self._Point = (0, 0)    # Coords on scene screen

    def InitImage(self):
        """
        Init decoration image.
        """
        pass

    def LoadImage(self, image_filename):
        """
        Load image.
        """
        self._Img = img.load_image(image_filename)
        return self._Img

    def Draw(self, scene):
        """
        Draw image on scene.
        :param scene: Scene object.
        """
        if scene:
            scene.DrawImage(self._Img, self._Point[0], self._Point[1])

    def GetImage(self):
        return self._Img

    def SetImage(self, Img_):
        self._Img = Img_

    def SetPoint(self, X_, Y_):
        self._Point = (X_, Y_)

    def GetPoint(self):
        return self._Point