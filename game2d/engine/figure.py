#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Abstract figure class.
"""

# --- Imports ---
import pygame

__version__ = (0, 0, 2, 1)


# --- Classes ---
class g2dFigure(pygame.sprite.Sprite):
    """
    Figure - sprite.
    """
    def __init__(self, scene=None):
        """
        Constructor.
        :param scene: Scene object.
        """
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        # Scene object
        self._Scene = scene

        # Cur figure image
        self.image = None
        # Position and size of figure
        self.rect = None

        # Image point (screen point)
        self._Point = (0, 0)

        # Map object
        self._Map = None
        # Figure map position
        self._Pos = (0, 0) 
        # Map cell symbol
        self._Cell = None
        # Cur ground map cell symbol
        self._Ground = None

        # Cur figure image index
        self._img_idx = 0
        # Cur figure state
        self._state = 0

    def update(self):
        """
        Update figure image.
        """
        pass

    def GetWidth(self):
        """
        Image width.
        """
        return self.rect.width

    def GetHeight(self):
        """
        Image height.
        """
        return self.rect.height

    def SetMap(self, map_object):
        """
        Set map object.
        """
        self._Map = map_object

    def SetPoint(self, point_x=0, point_y=0):
        """
        Set figure point.
        """
        self._Point = (point_x, point_y)
   
    def GetPoint(self):
        """
        Figure point.
        """
        return self._Point

    def SetGround(self, ground):
        self._Ground = ground

    def GetGround(self):
        return self._Ground

    def SetCell(self, cell):
        self._Cell = cell

    def GetPos(self):
        return self._Pos

    def SetPos(self, pos_x, pos_y):
        """
        Move figure to pos. 
        """
        if self._Ground:
            # 1. Keep old cell
            self._Map.SetCellByPos(self._Ground, self._Pos[0], self._Pos[1])
            # 2. Get new cell
            self._Ground = self._Map.GetCellByPos(pos_x, pos_y)
        # 3. Set cell new position
        self._Map.SetCellByPos(self._Cell, pos_x, pos_y)
        # 4. Keep position
        self._Pos = (pos_x, pos_y)
