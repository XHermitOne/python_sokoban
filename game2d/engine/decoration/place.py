#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль класов мест для ящика.
"""

import os
import os.path

from .. import decor

__version__ = (0, 0, 3, 1)

PLACE_IMG = None


class sokobanPlace(decor.g2dDecor):
    """
    Класс места для ящика.
    """
    def __init__(self, scene):
        """
        Конструктор.
        """
        decor.g2dDecor.__init__(self, scene)

        # Загрузить образы
        global PLACE_IMG
        if PLACE_IMG is None:
            PLACE_IMG = self.LoadImage(os.path.join(self._Scene.GetImgDir(), 'default',
                                                    'Environment', 'environment_04.png'))
        else:
            self.SetImage(PLACE_IMG)
