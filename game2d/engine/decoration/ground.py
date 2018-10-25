#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль класса почвы/земли.
"""

# === Подключение библиотек ===
import os
import os.path
import random

# Импортирование основных игровых модулей
import pygame

from game2d.engine import decor
from game2d.engine import map2d

__version__ = (0, 0, 2, 1)


GROUND_IMG = None


# --- Описания классов ---
class sokobanGround(decor.g2dDecor):
    """
    Класс почвы.
    """
    def __init__(self, scene):
        """
        Конструктор.
        """
        decor.g2dDecor.__init__(self, scene)

        # Загрузить образы
        global GROUND_IMG
        if GROUND_IMG is None:
            GROUND_IMG = self.LoadImage(os.path.join(self._Scene.GetImgDir(), 'default',
                                                     'Ground', 'ground_06.png'))
        else:
            self.SetImage(GROUND_IMG)

        # Определение образа
        # self.InitImage()

    def InitImage(self):
        """
        Инициализация образа.
        """
        img = pygame.Surface((map2d.MAP_CELL_WIDTH, map2d.MAP_CELL_HEIGHT))
        img.fill(0xD0C080)  # (208, 196, 128)

        # Расставить 4 точки в произвольном порядке
        for i in range(4):
            x = int(random.random()*map2d.MAP_CELL_WIDTH)
            y = int(random.random()*map2d.MAP_CELL_HEIGHT)
            if i:
                img.set_at((x, y), 0xA06040)
            else:
                img.set_at((x, y), 0xF0F0F0)
                img.set_at((x+1, y), 0xA06040)
                img.set_at((x+1, y+1), 0xA06040)
                img.set_at((x, y+1), 0xA06040)
        
        self._Img = img
        return img
