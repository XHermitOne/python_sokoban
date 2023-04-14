#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Модуль классов стены игры.
"""

import os
import os.path

from .. import decor

__version__ = (0, 0, 3, 1)

WALL_IMG = None


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
