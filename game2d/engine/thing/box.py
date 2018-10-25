#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Game box class.
"""

# --- Imports ---
import os
import os.path
import game2d.tools.image as img
import game2d.engine.map2d as map2d

import thing

__version__ = (0, 0, 2, 1)


# --- Classes ---
class sokobanBox(thing.g2dThing):
    """
    Sokoban box class.
    """
    # Images
    images = []

    def __init__(self, scene):
        """
        Constructor.
        """
        thing.g2dThing.__init__(self, scene)

        # Load images
        img_dir = self._Scene.GetImgDir()
        self.images = img.load_images(os.path.join(img_dir, 'default', 'Crates', 'crate_02.png'),
                                      os.path.join(img_dir, 'default', 'Crates', 'crate_01.png'))

    def update(self):
        """
        Update image.
        """
        self.image = self.images[self._img_idx]
        self.rect = self.image.get_rect()
        scene_point = self._Map.GetScreenScenePos()
        self.rect.left = self._Point[0]-scene_point[0]
        self.rect.top = self._Point[1]-scene_point[1]

    def SetPos(self, pos_x, pos_y):
        """
        Set position.    
        """
        thing.g2dThing.SetPos(self, pos_x, pos_y)
        if self._Ground == map2d.MAP_PLACE:
            self._img_idx = 1
        else:
            self._img_idx = 0

    def MoveToPos(self, pos_x, pos_y):
        """
        Move box to position.
        """
        cell = self._Map.GetCellByPos(pos_x, pos_y)
        if cell != map2d.MAP_WALL and cell != map2d.MAP_BOX:
            self._moveToPos(pos_x, pos_y)
            self.SetPos(pos_x, pos_y)

    def _moveToPos(self, pos_x, pos_y):
        """
        Step loop.
        @param pos_x, pos_y: Position.
        """
        dx, dy = ((pos_x-self._Pos[0])*4, (pos_y-self._Pos[1])*4)
        for phase in range(4):
            point = (self._Point[0]+dx, self._Point[1]+dy)

            self.rect.move_ip(point[0], point[1])

            self.SetPoint(point[0], point[1])
