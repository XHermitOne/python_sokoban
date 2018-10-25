#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль класов мест для ящика.
"""

# === Подключение библиотек ===
import os
import os.path

from game2d.engine import decor

# === Константы и спецификации ===
__version__ = (0, 0, 2, 1)

PLACE_IMG = None


# === Описания классов ===
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
