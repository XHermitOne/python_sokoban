#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tools functions.
"""


def Limit(value, minimum, maximum):
    """ 
    Limit minimum and maximum value.
    :param value: Numeric value.
    :param minimum: Minimum value.
    :param maximum: Maximum value.
    """
    return max(minimum, min(maximum, value))


def LogPrintWin(text):
    """
    Print text in windows cp1251 codepage.
    :param text: Text.
    """
    txt = unicode(text, 'CP1251')
    txt = txt.encode('CP866')
    print(txt)
