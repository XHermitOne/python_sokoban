#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Game hero class.
"""

# --- Imports ---
import os
import os.path
import pygame.time
import game2d.tools.image as img
import game2d.engine.map2d as map2d

import person

__version__ = (0, 0, 2, 1)


# --- Classes ---
class sokobanHero(person.g2dPersonage):
    """
    Sokoban game hero class.
    """

    def __init__(self, scene):
        """
        Constructor.
        """
        person.g2dPersonage.__init__(self, scene)

        # Moving phase
        self._MovingPhase = 0
        # State code
        self._State = 0
        # Step index
        self._StateStep = 1
        # Horizontal speed rate
        self._HorizSpeed = 4
        # Vertical speed rate
        self._VertSpeed = 4

        # Load images
        self.images = list()
        img_dir = self._Scene.GetImgDir()
        self.images += img.load_images(os.path.join(img_dir, 'default', 'Player', 'player_15.png'),
                                       os.path.join(img_dir, 'default', 'Player', 'player_16.png'),
                                       os.path.join(img_dir, 'default', 'Player', 'player_17.png'))

        self.images += [img.flip_horiz_img(self.images[0]),
                        img.flip_horiz_img(self.images[1]),
                        img.flip_horiz_img(self.images[2])]

        self.images += [img.rotate_img(self.images[3], img.ANGLE_270),
                        img.rotate_img(self.images[4], img.ANGLE_270),
                        img.rotate_img(self.images[5], img.ANGLE_270)]

        self.images += [img.rotate_img(self.images[3], img.ANGLE_90),
                        img.rotate_img(self.images[4], img.ANGLE_90),
                        img.rotate_img(self.images[5], img.ANGLE_90)]

        # Init image
        self.image = self.images[self._img_idx]
        self.rect = self.image.get_rect()

    def RunToLeft(self):
        """
        Move hero to Left.
        """        
        # New moving phase
        self._MovingPhase = 3
        self.MoveToPos(self._Pos[0]-1, self._Pos[1])

    def RunToRight(self):
        """
        Move hero to right.
        """        
        # New moving phase
        self._MovingPhase = 0
        self.MoveToPos(self._Pos[0]+1, self._Pos[1])

    def RunToUp(self):
        """
        Move hero to up.
        """        
        self._MovingPhase = 6
        self.MoveToPos(self._Pos[0], self._Pos[1]-1)

    def RunToDown(self):
        """
        Move hero to down.
        """        
        self._MovingPhase = 9
        self.MoveToPos(self._Pos[0], self._Pos[1]+1)

    def UseIt(self):
        pass

    def DoIt(self):
        pass

    def Die(self):
        pass

    def update(self):
        """
        Update hero image.
        """
        self._img_idx = self._MovingPhase+self._State
        self.image = self.images[self._img_idx]

    def SetPoint(self, point_x=0, point_y=0):
        """
        Set figure point.
        """
        self._Point = (point_x, point_y)

        scene_point = self._Map.GetScreenScenePos()
        self.rect.left = self._Point[0]-scene_point[0]
        self.rect.top = self._Point[1]-scene_point[1]
        
    def MoveSceneTo(self):
        """
        Move scene.
        """
        direction = (int(self._Point[0] >= self._Map._Scene._ScreenRect[2]),
                     int(self._Point[1] >= self._Map._Scene._ScreenRect[3]))
        self._Map.MoveScene(direction)

        direction = (-int(self._Point[0] <= self._Map._ScreenScenePos[0]),
                     -int(self._Point[1] <= self._Map._ScreenScenePos[1]))
        self._Map.MoveScene(direction)

    def MoveToPoint(self, point_x, point_y):
        """
        Move personage to point (point_x, point_y).
        @param point_x, point_y: New point.
        """
        cell = self._Map.GetCellByPoint(point_x, point_y)
        if cell != map2d.MAP_WALL:
            self.rect.move_ip(point_x-self._Point[0], point_y-self._Point[1])
            self.SetPoint(point_x, point_y)

    def MoveToPos(self, pos_x, pos_y):
        """
        Move personage to position (pos_x, pos_y).
        @param pos_x, pos_y: New position.
        """
        cell = self._Map.GetCellByPos(pos_x, pos_y)
        if cell != map2d.MAP_WALL:
            dx, dy = (pos_x-self._Pos[0], pos_y-self._Pos[1])
            if cell == map2d.MAP_BOX:
                to_pos = (pos_x+dx, pos_y+dy)
                box = self._Map.GetObjByPos(pos_x, pos_y)

                if box:
                    box.MoveToPos(to_pos[0], to_pos[1])
                if self._Map.GetCellByPos(pos_x, pos_y) != map2d.MAP_BOX:
                    self._moveToPos(pos_x, pos_y)
                    self.SetPos(pos_x, pos_y)
            else:
                self._moveToPos(pos_x, pos_y)
                self.SetPos(pos_x, pos_y)

    def _moveToPos(self, pos_x, pos_y):
        """
        Move steps.
        @param pos_x, pos_y: Position.
        """
        dx, dy = ((pos_x-self._Pos[0])*4, (pos_y-self._Pos[1])*4)
        for phase in range(4):
            point = (self._Point[0]+dx, self._Point[1]+dy)
            self._State += self._StateStep
            if self._State >= 2 or self._State <= 0:
                self._StateStep = -self._StateStep

            self.update()
            self.rect.move_ip(point[0], point[1])
            self.SetPoint(point[0], point[1])

            self._Scene.Draw()
            pygame.time.delay(40)
