#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Game map classes.
"""

# --- Imports ---
import os
import os.path

from game2d.tools import tools
from game2d.tools import log

# --- Constants ---
# Scene size (map cells)
MAP_SCENE_WIDTH = 20
MAP_SCENE_HEIGHT = 16

# Map cell size (points)
MAP_CELL_WIDTH = 64
MAP_CELL_HEIGHT = 64

# Move scene direction on map
NO_MOVE_SCENE = (0, 0)
MOVE_SCENE_RIGHT = (1, 0)
MOVE_SCENE_LEFT = (-1, 0)
MOVE_SCENE_UP = (0, -1)
MOVE_SCENE_DOWN = (0, 1)

# --- Map symbols ---
MAP_GROUND = '.'
MAP_NONE = ' '

MAP_WALL = '#'

MAP_BOX = 'O' 
MAP_PLACE = '*' 

MAP_HERO = '@'


# --- Classes ---
class g2dMap:
    """
    Abstract map class.
    """
    
    def __init__(self):
        """
        Constructor.
        """
        self._Level = 1     # Level number
        self._MapDir = ''   # Map resources directory path

        self._MapImg = []   # Map data
        self._Scene = None  # Scene object
        # Scene size (map cells)
        self._SceneSize = (MAP_SCENE_WIDTH, MAP_SCENE_HEIGHT) 

        # Map position on screen
        self._MapOffset = (0, 0)
        # Left-top scene position (map cells)
        self._ScenePos = (0, 0)
        # Left-top scen position (screen points)
        self._ScreenScenePos = (0, 0)

        # Map size
        self._Size = (0, 0)

    def Load(self, map_filename):
        """
        Load map.
        :param map_filename: Map resource file.
        """
        pass

    def SetScene(self, scene=None, scene_x=0, scene_y=0):
        """
        Set scene object.
        :param scene: Scene object.
        :param scene_x, scene_y: Left-top position scene (map cells).
        """
        self._Scene = scene
        self._ScenePos = (scene_x, scene_y)
        self._ScreenScenePos = (scene_x*MAP_CELL_WIDTH, scene_y*MAP_CELL_HEIGHT)

    def MoveSceneToPos(self, pos_x,pos_y):
        """
        Move scene object on map.
        :param pos_x, pos_y: Position coordinates. 
        """
        self._ScenePos = (pos_x, pos_y)
        self._ScreenScenePos = (pos_x*MAP_CELL_WIDTH, pos_y*MAP_CELL_HEIGHT)

    def MoveScene(self, direction):
        """
        Move scene object on map.
        :param direction: Move direction. 
        """
        try:
            if not direction[0] and not direction[0]:
                return
            # Calculate new position
            self._ScenePos = (tools.Limit(self._ScenePos[0]+direction[0]*self._SceneSize[0],
                              0, self._Size[0]-self._SceneSize[0]),
                              tools.Limit(self._ScenePos[1]+direction[1]*self._SceneSize[1],
                              0, self._Size[1]-self._SceneSize[1]),)
            self._ScreenScenePos = (self._ScenePos[0]*MAP_CELL_WIDTH,
                                    self._ScenePos[1]*MAP_CELL_HEIGHT)
        except:
            log.fatal(u'ERROR: Move scene object.')

    def SceneMap(self):
        """
        View port scene.
        """
        try:
            scene_map = []
            for i in range(self._SceneSize[1]):
                scene_map.append(self._MapImg[self._ScenePos[1] + i][self._ScenePos[0]:self._ScenePos[0] + self._SceneSize[0]])
            return scene_map
        except:
            log.fatal(u'ERROR: View port map scene.')
            return []

    def GetMapImage(self):
        """
        Map data.
        """
        return self._MapImg

    def SetMapImage(self, map_image=None):
        """
        Set map data.
        :param map_image: Map data.
        """
        if map_image is None:
            map_image = list()

        self._MapImg = map_image
        # Find map width
        width = max([len(x.strip()) for x in self._MapImg])
        # Set map size 
        self._Size = (width, len(self._MapImg))

    def GetScenePos(self):
        """
        Scene object position.
        """
        return self._ScenePos

    def GetScreenScenePos(self):
        """
        Scene object screen posotion.
        """
        return self._ScreenScenePos

    def GetCellByPos(self, pos_x, pos_y):
        """
        Get cell symbol by coords.
        :param pos_x, pos_y: Position.
        """
        return self._MapImg[pos_y][pos_x]

    def SetCellByPos(self, cell, pos_x, pos_y):
        """
        Set cell symbol on map.
        :param cell: Cell symbol.
        :param pos_x, pos_y: Position.
        """
        if self._MapImg and cell:
            self._MapImg[pos_y] = self._MapImg[pos_y][:pos_x]+cell+self._MapImg[pos_y][(pos_x+1):]

    def GetCellByPoint(self, point_x, point_y):
        """
        Get cell symbol by screen point.
        :param point_x, point_y: Point coords.
        """
        return self._MapImg[(point_y-self._MapOffset[1])/MAP_CELL_HEIGHT][(point_x-self._MapOffset[0])/MAP_CELL_WIDTH]

    def GetObjByPos(self, pos_x, pos_y):
        """
        Get game object by position.
        :param pos_x, pos_y: Position.
        """
        obj = None
        pos = (pos_x, pos_y)
        if self._Scene:
            for cur_obj in self._Scene.GetAll():
                if cur_obj.GetPos() == pos:
                    obj = cur_obj
                    break
        return obj

    def GetLevel(self):
        return self._Level

    def SetMapDir(self, map_dir):
        self._MapDir = map_dir

    def LoadNext(self):
        """
        Load next level map.
        :return: True/False.
        """
        return self.LoadLevel(self._Level+1)

    def LoadCur(self):
        """
        Reload cur level.
        :return: True/False.
        """
        return self.LoadLevel(self._Level)
    
    def LoadLevel(self, level=1):
        """
        Load level map by number.
        :param level: Level number.
        :return: True/False.
        """
        self._Level = level
        next_map_file = self._genMapFileName(self._Level)
        return self.Load(next_map_file)

    def _genMapFileName(self, level=1):
        """
        Generate map file name by level number.
        """
        return os.path.join(self._MapDir, '%04u.map' % level)


class sokobanMap(g2dMap):
    """
    Sokoban map class.
    """
    def __init__(self):
        """
        Constructor.
        """
        g2dMap.__init__(self)

    def Load(self, map_filename):
        """
        Load map.
        :param map_filename: Map resource file name.
        :return: True/False.
        """
        if map_filename is None:
            return False

        map_file = None
        try:
            map_file = open(map_filename)
            map_img = map_file.readlines()
            map_file.close()
            map_img = [x.replace('\n', '').replace('\r', '') for x in map_img]
    
            self.SetMapImage(map_img)
        except:
            if map_file:
                map_file.close()
            return False
        return True        

    def Center(self):
        """
        Center map in screen.
        """
        if self._Scene is None:
            self._MapOffset = (0, 0)
            return

        size_point = (self._Scene.GetScreenRect().width,
                      self._Scene.GetScreenRect().height)

        x_offset = (size_point[0]-(MAP_CELL_WIDTH*self._Size[0]))/2
        y_offset = (size_point[1]-(MAP_CELL_HEIGHT*self._Size[1]))/2
        self._MapOffset = (x_offset, y_offset)

        if self._Scene:
            self._Scene.SetAllOffset(self._MapOffset)
