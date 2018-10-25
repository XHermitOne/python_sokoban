#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Game hero class.
"""

# --- Imports ---
import os
import os.path
import pygame.time

from game2d.tools import image as img
from game2d.engine import map2d
from game2d.tools import log

import person

__version__ = (0, 0, 2, 1)

HERO_MOVE_DELAY = 40


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
        self._HorizSpeed = map2d.MAP_CELL_WIDTH / 4
        # Vertical speed rate
        self._VertSpeed = map2d.MAP_CELL_WIDTH / 4

        # Load images
        self.images = list()
        img_dir = self._Scene.GetImgDir()

        # To Right move sprites
        self.images += img.load_images(os.path.join(img_dir, 'default', 'Player', 'player_18.png'),
                                       os.path.join(img_dir, 'default', 'Player', 'player_17.png'),
                                       os.path.join(img_dir, 'default', 'Player', 'player_19.png'))

        # To Left move sprites
        self.images += img.load_images(os.path.join(img_dir, 'default', 'Player', 'player_21.png'),
                                       os.path.join(img_dir, 'default', 'Player', 'player_20.png'),
                                       os.path.join(img_dir, 'default', 'Player', 'player_22.png'))

        # To Up move sprites
        self.images += img.load_images(os.path.join(img_dir, 'default', 'Player', 'player_09.png'),
                                       os.path.join(img_dir, 'default', 'Player', 'player_08.png'),
                                       os.path.join(img_dir, 'default', 'Player', 'player_10.png'))

        # To Down move sprites
        self.images += img.load_images(os.path.join(img_dir, 'default', 'Player', 'player_06.png'),
                                       os.path.join(img_dir, 'default', 'Player', 'player_05.png'),
                                       os.path.join(img_dir, 'default', 'Player', 'player_07.png'))

        # Init image
        self.image = self.images[self._img_idx]
        self.rect = self.image.get_rect()

    def RunToLeft(self):
        """
        Move hero to Left.
        """
        log.debug(u'Движение влево')
        # New moving phase
        self._MovingPhase = 3
        self.MoveToPos(self._Pos[0]-1, self._Pos[1])

    def RunToRight(self):
        """
        Move hero to right.
        """        
        log.debug(u'Движение вправо')
        # New moving phase
        self._MovingPhase = 0
        self.MoveToPos(self._Pos[0]+1, self._Pos[1])

    def RunToUp(self):
        """
        Move hero to up.
        """        
        log.debug(u'Движение вверх')
        self._MovingPhase = 6
        self.MoveToPos(self._Pos[0], self._Pos[1]-1)

    def RunToDown(self):
        """
        Move hero to down.
        """        
        log.debug(u'Движение вниз')
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
                    # box.MoveToPos(pos_x, pos_y)
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
        dx, dy = ((pos_x-self._Pos[0])*self._HorizSpeed,
                  (pos_y-self._Pos[1])*self._VertSpeed)
        log.debug(u'Приращение в точках [%d : %d]' % (dx, dy))
        for phase in range(4):
            point = (self._Point[0]+dx, self._Point[1]+dy)
            self._State += self._StateStep
            if self._State >= 2 or self._State <= 0:
                self._StateStep = -self._StateStep

            self.update()
            self.rect.move_ip(point[0], point[1])
            self.SetPoint(point[0], point[1])

            self._Scene.Draw()
            pygame.time.delay(HERO_MOVE_DELAY)
