#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Scene classes.
"""

# --- Imports ---
import os
import os.path
import pygame
# import pygame.locals

from ..tools import image as img
from ..tools import log

from .decoration import wall
from .thing import box
from .decoration import place
from .decoration import ground

from .person import hero

from . import map2d

__version__ = (0, 0, 3, 1)

BLACK_COLOR = pygame.Color(0, 0, 0, 0)
DEFAULT_SCREEN_COLOR = BLACK_COLOR

SCENE_WIDTH = map2d.MAP_CELL_WIDTH * map2d.MAP_SCENE_WIDTH
SCENE_HEIGHT = map2d.MAP_CELL_HEIGHT * map2d.MAP_SCENE_HEIGHT

DEFAULT_IMAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                 'img', 'kenney', 'PNG')


# --- Classes ---
class g2dScene:
    """
    Abstract scene class.
    """
    def __init__(self):
        # Image directory path
        self._ImgDir = None
        # Screen object
        self._Screen = None
        # Screen size
        self._ScreenRect = pygame.Rect(0, 0, SCENE_WIDTH, SCENE_HEIGHT)
        # Screen parameters
        self._WinStyle = 0
        self._BestDepth = None
        # Background image
        self._Background = None
        self._BackgroundImg = None

        # Font
        self._Font = None
        self._FontFileName = ''

        # Clock
        self._Clock = None

        # Hero
        self._Hero = None

        # Game things
        self._Things = pygame.sprite.Group()
        # Game tools
        self._Tools = None
        # Game persons
        self._Persons = pygame.sprite.Group()

        self._All = pygame.sprite.RenderUpdates()

        # Decoration list
        self._Decors = []

    def SetImgDir(self, image_dir=DEFAULT_IMAGE_DIR):
        self._ImgDir = image_dir

    def GetImgDir(self):
        return self._ImgDir

    def GetScreenRect(self):
        return self._ScreenRect

    def SetFont(self, font_filename=None, font_size=20):
        """
        Set font.
        :param font_filename: Font file name.
        :param font_size: Font size.
        """
        if font_filename:
            self._FontFileName = os.path.join(self._ImgDir, font_filename)
        try:
            self._Font = pygame.font.Font(self._FontFileName, font_size)
        except:
            log.fatal(u'Ошибка установки шрифта <%s>' % self._FontFileName)

    def GetFont(self):
        return self._Font

    def DrawTextXY(self, text, x, y, color=(255, 255, 255)):
        """
        Draw text on scene background.
        :param text: Text.
        :param x, y: Draw coords.
        :param color: RGB color.
        """
        if self._Font and self._Background:
            txt = self._Font.render(text, 0, color)
            self._Background.blit(txt, (x, y))

    def SetAllOffset(self, offset=(0, 0)):
        """
        Set all sprites offset.
        :param offset: Offset (point).
        """
        # Sprites
        if self._All:
            for any in self._All:
                any.SetPoint(any.GetPoint()[0]+offset[0],
                             any.GetPoint()[1]+offset[1])
        # Decorations
        if self._Decors:        
            for any in self._Decors:
                any.SetPoint(any.GetPoint()[0]+offset[0],
                             any.GetPoint()[1]+offset[1])

    def RegDecor(self, decor):
        """
        Registry decoration.
        """
        if decor:
            self._Decors.append(decor)

    def DrawImage(self, image, x, y):
        """
        Draw image on scene background.
        :param image: Image.
        :param x, y: Draw point.
        """
        try:
            if self._Background:
                self._Background.blit(image, (x, y))
        except:
            log.fatal(u'ERROR: Draw image %s to point (%d, %d)!' % (str(image), x, y))

    def RefreshScreen(self):
        """
        Обновление экрана сцены.
        """
        if self._Background:
            self._Screen.blit(self._Background, (0, 0))
        else:
            log.warning(u'Не определен фон')
        pygame.display.flip()

    def DrawBackground(self, background_filename=None):
        """
        Отрисовка фона сцены.
        :param background_filename: Background image file name.
        :return: True/False.
        """
        try:
            if background_filename and os.path.exists(background_filename):
                self._BackgroundImg = pygame.image.load(os.path.join(self._ImgDir, background_filename)).convert()
            else:
                if self._Background:
                    self._Background.fill(DEFAULT_SCREEN_COLOR)
                else:
                    log.warning(u'Не определен фон сцены')
                return True

            self._Background = pygame.Surface(self._ScreenRect.size, flags=pygame.SRCALPHA)
            # X
            for x in range(0, self._ScreenRect.width, self._BackgroundImg.get_width()):
                # Y
                for y in range(0, self._ScreenRect.height, self._BackgroundImg.get_height()):
                    self._Background.blit(self._BackgroundImg, (x, y))
            return True
        except:
            log.fatal(u'Ошибка отрисовки фона сцены')
            return False

    def DrawDecor(self):
        """
        Draw all decorations.
        """
        if self._Decors:
            for decor in self._Decors:
                decor.Draw(self)
            
    def FillScreen(self):
        """
        Full screen.
        """
        self.DrawBackground()
        self.DrawDecor()
        self.RefreshScreen()

    def RegSprites(self):
        """
        Registry all sprites.
        """
        pass

    def Init(self):
        """
        Scene initialization.
        :return: True/False.
        """
        try:
            # pygame init
            pygame.init()
            # Display mode
            self._WinStyle = 0  # Window style
            self._BestDepth = pygame.display.mode_ok(self._ScreenRect.size,
                                                     self._WinStyle, 32)
            self._Screen = pygame.display.set_mode(self._ScreenRect.size,
                                                   self._WinStyle, self._BestDepth)
            # Window title
            pygame.display.set_caption('SOKOBAN')
            # Icon
            # icon=pygame.transform.scale(img,(32,32))
            # pygame.display.set_icon(icon)
            # Mouse
            pygame.mouse.set_visible(0)
            # Background
            # if background_filename:
            #    self._BackgroundImg=pygame.image.load(background_filename).convert()

            # Clock
            self._Clock = pygame.time.Clock()

            # --- Object registry ---
            self.RegSprites()

            return True
        except:
            log.fatal(u'ERROR: Scene initialisation.')
            return False

    def Draw(self):
        """
        Отрисовка сцены.
        """
        # draw the scene
        # clear/erase the last drawn sprites
        self._All.clear(self._Screen, self._Background)
        
        # update all the sprites
        self._All.update()

        # draw the scene
        dirty = self._All.draw(self._Screen)
        pygame.display.update(dirty)
        # cap the framerate
        self._Clock.tick(40)

    def ClearSprites(self):
        """
        Delete all sprites.
        """
        self._Things.empty()
        self._Persons.empty()
        self._All.empty()

    def ClearDecors(self):
        """
        Delete all decorations.
        """
        self._Decors = list()

    def ClearScreen(self):
        """
        Очистка экрана.
        """
        if self._Screen:
            self._Screen.fill(DEFAULT_SCREEN_COLOR)
        else:
            log.warning(u'Не определен экран для сцены')

    def Clear(self):
        """
        Полная очистка сцены.
        :return:
        """
        self.ClearSprites()
        self.ClearDecors()
        self.FillScreen()

    def GetHero(self):
        """
        Hero.
        """
        return self._Hero

    def GetThings(self):
        return self._Things

    def GetTools(self):
        return self._Tools

    def GetPersons(self):
        return self._Persons

    def GetAll(self):
        """
        All scene objects.
        """
        return self._All


# ------------------------------------------------------------------------------
class sokobanScene(g2dScene):
    """
    Sokoban scene class.
    """
    def __init__(self):
        """
        Constructor.
        """
        g2dScene.__init__(self)

    def RegSprites(self):
        """
        Sprite registry.
        """
        # Box
        box.sokobanBox.containers = self._Things, self._All

        # Hero
        hero.sokobanHero.containers = self._Persons, self._All

    def CreateObjects(self, map_object):
        """
        Create all game objects.
        :param map_object: Map object.
        """
        try:
            map_img = map_object.GetMapImage()
            # Rows
            for i_row in range(len(map_img)):
                row = map_img[i_row]
                # Columns
                len_row = len(row)
                i_col = 0
                while i_col < len_row:
                    cell = row[i_col]
                    x = i_col*map2d.MAP_CELL_WIDTH
                    y = i_row*map2d.MAP_CELL_HEIGHT
                    if cell in self._createObjectDict:
                        new_obj = self._createObjectDict[cell](self, map_object, cell, x, y, i_col, i_row)
                    elif cell is None:
                        pass
                    else:
                        log.debug(u'Map cell symbol: %s type: %s' % (cell, type(cell)))
                    i_col += 1
            return True
        except:
            log.fatal(u'ERROR: Create game objects.')
            return False
        
    def _addGround(self, map_object, cell, x, y, column, row):
        """
        Create ground object.
        """
        cur_ground = ground.sokobanGround(self)
        cur_ground.SetPoint(x, y)
        self.RegDecor(cur_ground)
        return cur_ground

    def _addWall(self, map_object, cell, x, y, column, row):
        """
        Create wall object.
        """
        cur_wall = wall.sokobanWall(self)
        cur_wall.SetPoint(x, y)
        self.RegDecor(cur_wall)
        return cur_wall
        
    def _addBox(self, map_object, cell, x, y, column, row):
        """
        Create box object.
        """
        cur_box = box.sokobanBox(self)
        cur_box.SetMap(map_object)
        cur_box.SetPoint(x, y)
        cur_box.SetCell(cell)
        cur_box.SetPos(column, row)
        cur_box.SetGround(map2d.MAP_GROUND)
        self._addGround(map_object, map2d.MAP_GROUND, x, y, column, row)
        return cur_box

    def _addPlace(self, map_object, cell, x, y, column, row):
        """
        Create place object.
        """
        cur_place = place.sokobanPlace(self)
        cur_place.SetPoint(x, y)
        self.RegDecor(cur_place)
        return cur_place
        
    def _addHero(self, map_object, cell, x, y, column, row):
        """
        Create hero object.
        """
        self._Hero = hero.sokobanHero(self)
        self._Hero.SetMap(map_object)
        self._Hero.SetPoint(x, y)
        self._Hero.SetPos(column, row)
        self._Hero.SetCell(cell)
        self._Hero.SetGround(map2d.MAP_GROUND)
        self._addGround(map_object, map2d.MAP_GROUND, x, y, column, row)
        return self._Hero
  
    _createObjectDict = {map2d.MAP_GROUND: _addGround,
                         map2d.MAP_WALL: _addWall,
                         map2d.MAP_BOX: _addBox,
                         map2d.MAP_PLACE: _addPlace,
                         map2d.MAP_HERO: _addHero,
                         }
    
    def TitlePage(self):
        """
        Title.
        """
        self._Background = pygame.Surface(self._ScreenRect.size)
        # Picture
        # artefact = img.load_image(os.path.join(self._ImgDir, 'artefact.png'))
        # x, y = img.calc_center_xy(self._ScreenRect.width,self._ScreenRect.height,
        #                         artefact.get_width(), artefact.get_height())
        # self.DrawImage(artefact, x, y)

        txt = 'SOKOBAN'
        self.SetFont(None, 32)
        w, h = self._Font.size(txt)
        x, y = img.calc_center_xy(self._ScreenRect.width, self._ScreenRect.height, w, h)
        self.DrawTextXY(txt, x, 50, (224, 192, 128))

        txt = 'Press any key...'
        self.SetFont(None, 12)
        w, h = self._Font.size(txt)
        x, y = img.calc_center_xy(self._ScreenRect.width, self._ScreenRect.height, w, h)
        self.DrawTextXY(txt, x, self._ScreenRect.height-70, (224, 192, 128))

        txt = 'Help: ESC-break level; F10-exit'
        self.SetFont(None, 12)
        w, h = self._Font.size(txt)
        # x,y=img.calc_center_xy(self._ScreenRect.width,self._ScreenRect.height,w,h)
        self.DrawTextXY(txt, 5, self._ScreenRect.height-20, (224, 192, 128))
        
        self.RefreshScreen()
        while pygame.event.wait().type != pygame.KEYDOWN:
            pass

    def BacksidePage(self):
        """
        Game over page.
        """
        self._Background = pygame.Surface(self._ScreenRect.size)
        artefact = img.load_image(os.path.join(self._ImgDir, 'artefact.png'))
        x, y = img.calc_center_xy(self._ScreenRect.width, self._ScreenRect.height,
                                  artefact.get_width(), artefact.get_height())
        self.DrawImage(artefact, x, 50)    

        txt = 'GAME OVER...'
        self.SetFont(None, 16)
        w, h = self._Font.size(txt)
        x, y = img.calc_center_xy(self._ScreenRect.width, self._ScreenRect.height, w, h)
        self.DrawTextXY(txt, x, self._ScreenRect.height-150, (224, 192, 128))

        self.RefreshScreen()
        while pygame.event.wait().type != pygame.KEYDOWN:
            pass
