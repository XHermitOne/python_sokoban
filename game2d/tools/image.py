#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Функции работы с изображениями.
"""

import os.path
import pygame
import pygame.locals


__version__ = (0, 0, 6, 2)


def load_image(img_filename, do_convert=True):
    """
    Загрузить изображение из файла.
    @param img_filename: Полное имя файла изображения.
    @param do_convert: Производить автоматически конвертацию?
    @return: Объект изображения.
    """
    try:
        if (isinstance(img_filename, str) or isinstance(img_filename, unicode)) and os.path.exists(img_filename):
            img = pygame.image.load(img_filename)
            return img.convert_alpha() if do_convert else img
        else:
            print(u'ERROR. File <%s> not found' % img_filename)
    except pygame.error: 
        raise SystemExit(u'ERROR: Load image <%s> %s' % (img_filename, pygame.get_error()))
    return None


def save_image(img, img_filename, rewrite=True):
    """
    Сохранить изображение в файл.
    @param img: Объект изображения.
    @param img_filename: Полное имя файла изображения.
    @param rewrite: Перезаписать, если уже существует?
    @return: True/False.
    """
    try:
        if type(img_filename) in (unicode, str) and os.path.exists(img_filename) and rewrite:
            os.remove(img_filename)
        elif type(img_filename) in (unicode, str) and os.path.exists(img_filename) and not rewrite:
            print(u'WARNING. File <%s> exists. Rewrite banned' % img_filename)
            return False

        pygame.image.save(img, img_filename)
        return True
    except pygame.error:
        raise SystemExit(u'ERROR: Save image <%s> %s' % (img_filename, pygame.get_error()))
    return None


def load_images(*img_filenames):
    """
    Зугрузка нескольких изображений.
    @param img_filenames: Список файлов изображений.
    """
    images = []
    for img_file in img_filenames:
        images.append(load_image(img_file))
    return images


def flip_horiz_img(img):
    """
    Отразить изображение по горизонтальной оси.
    """
    return pygame.transform.flip(img, True, False) 


def flip_vert_img(img):
    """
    Отразить изображение по вертикальной оси.
    """
    return pygame.transform.flip(img, False, True) 


# Angles gradus
ANGLE_90 = 90
ANGLE_180 = 180
ANGLE_270 = 270


def rotate_img(img, angle=0):
    """
    Поворот изображения на угол.
    @param img: Объект изображения.
    @param angle: Угол в градусах.
    """
    return pygame.transform.rotate(img, angle)


def calc_center_xy(win_width, win_height, img_width, img_height):
    """
    Расчитать координаты изображения для размещения по центру окна.
    @param win_width: Ширина главного окна.
    @param win_height: Высота главного окна.
    @param img_width: Размер изображения. Ширина.
    @param img_height: Размер изображения. Высота.
    @return: (X, Y) - Координаты изображения для отображения по центру окна.
    """
    x_offset = (win_width - img_width) / 2
    y_offset = (win_height - img_height) / 2
    return x_offset, y_offset


def image_scale(img, scale=2):
    """
    Масштабировать изображение.
    @param img: Объект изображения.
    @param scale: Коэффициент масштабирования.
    @return: Новый смасштабированный объект изображения.
    """
    img_width, img_height = img.get_size()
    # create a 2x bigger image than self.image
    return pygame.transform.scale(img, (int(img_width * scale), int(img_height * scale)))


def load_image_fragment(img_filename, x, y, width, height, do_convert=True):
    """
    Загрузка фрагмента/кадра из файла образа.
    @param img_filename: Полное имя файла изображения.
    @param x: Координата X левого-верхнего угла фрагмента.
    @param y: Координата Y левого-верхнего угла фрагмента.
    @param width: Ширина фрагмента.
    @param height: Высота фрагмента.
    @param do_convert: Производить автоматически конвертацию?
    @return: Объект изображения фрагмента. None в случае ошибки.
    """
    img = load_image(img_filename, do_convert)
    if img:
        # ВНИМАНИЕ! У нового образа фон д.б. прозрачный иначе происходит закрашивание фона
        # при использовании blit                     |                      |
        #                                            v                      v
        fragment = pygame.Surface((width, height), flags=pygame.SRCALPHA, depth=32)
        if do_convert:
            fragment = fragment.convert_alpha()

        fragment.blit(img, (0, 0), (x, y, width, height))
        return fragment.convert_alpha() if do_convert else fragment
    return None


def load_image_fragment_scale(img_filename, x, y, width, height, scale=1, do_convert=True):
    """
    Загрузка фрагмента/кадра из файла образа с масштабированием.
    @param img_filename: Полное имя файла изображения.
    @param x: Координата X левого-верхнего угла фрагмента.
    @param y: Координата Y левого-верхнего угла фрагмента.
    @param width: Ширина фрагмента.
    @param height: Высота фрагмента.
    @param scale: Коэффициент масштабирования.
    @param do_convert: Производить автоматически конвертацию?
    @return: Объект изображения фрагмента. None в случае ошибки.
    """
    img = load_image_fragment(img_filename, x, y, width, height, do_convert=do_convert)
    if img and scale > 1:
        img = image_scale(img, scale)
    return img


def resize_image(img, width, height, do_convert=True):
    """
    Изменение размеров изображения
    @param img: Объект изображения.
    @param width: Новая ширина изображения.
    @param height: Новая высота изображения.
    @param do_convert: Производить автоматически конвертацию?
    @return: Объект переразмеренного образа или None - ошибка.
    """
    if img:
        # ВНИМАНИЕ! У нового образа фон д.б. прозрачный иначе происходит закрашивание фона
        # при использовании blit                     |                      |
        #                                            v                      v
        new_img = pygame.Surface((width, height), flags=pygame.SRCALPHA, depth=32)
        if do_convert:
            new_img = new_img.convert_alpha()

        img_width, img_height = img.get_size()
        new_img.blit(img, (0, 0), (0, 0, img_width, img_height))
        return new_img
    return None


def offset_image(img, offset_x, offset_y, do_convert=True):
    """
    Сделать смещение изображения в другую точку.
    @param img: Объект изображения.
    @param offset_x: Смещение координаты X левого-верхнего угла, относительно текущего.
    @param offset_y: Смещение координаты Y левого-верхнего угла, относительно текущего.
    @param do_convert: Производить автоматически конвертацию?
    @return: Объект изображения фрагмента. None в случае ошибки.
    """
    if img:
        img_width, img_height = img.get_size()
        # ВНИМАНИЕ! У нового образа фон д.б. прозрачный иначе происходит закрашивание фона
        # при использовании blit                     |                      |
        #                                            v                      v
        new_img = pygame.Surface((img_width, img_height), flags=pygame.SRCALPHA, depth=32)
        if do_convert:
            new_img = new_img.convert_alpha()

        new_img.blit(img, (offset_x, offset_y), (0, 0, img_width, img_height))
        return new_img
    return None
