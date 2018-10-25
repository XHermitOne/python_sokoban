#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Модуль классов стены игры.
"""

# === Подключение библиотек ===
import os
import os.path

from game2d.engine import decor

# === Константы и спецификации ===
__version__ = (0, 0, 2, 1)

WALL_IMG = None


# === Описания классов ===
class sokobanWall(decor.g2dDecor):
    """
    Класс стены.
    """
    def __init__(self, scene):
        """
        Конструктор.
        """
        decor.g2dDecor.__init__(self, scene)

        # Загрузить образы
        global WALL_IMG
        if WALL_IMG is None:
            WALL_IMG = self.LoadImage(os.path.join(self._Scene.GetImgDir(),
                                                   'default', 'Blocks', 'block_01.png'))
        else:
            self.SetImage(WALL_IMG)
