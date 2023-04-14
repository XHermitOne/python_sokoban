# !/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
File working functions.
"""

import os
import os.path
import shutil 

__version__ = (0, 0, 1, 1)


def getRelativePath(path):
    """
    Get relative path.
    :param path: Path.
    """
    if not path:
        return path
    # ATTENTION!!! All sleshes UNIX type!
    cur_work_dir = os.getcwd().replace('\\', '/').lower()
    path = path.replace('\\', '/').lower()
    return path.replace(cur_work_dir, '.')


def getAbsolutePath(path):
    """
    Get absolute path.
    :param path: Path.
    """
    if not path:
        return path
    cur_work_dir = os.getcwd().replace('\\', '/').lower()
    path = path.replace('\\', '/').lower()
    return path.replace('./', cur_work_dir + '/')


def copyFile(src_filename, dst_filename):
    """
    Copy file with path.
    """
    if os.path.isfile(src_filename):
        dst_path = os.path.dirname(dst_filename)
        if not os.path.isdir(dst_path):
            os.makedirs(dst_path)
        shutil.copyfile(src_filename, dst_filename)
        return True
    return False


def createBAKFile(filename):
    """
    Create backup *.bak file.

    :param filename: File name.
    """
    bak_file_name = filename + '.bak'
    return copyFile(filename, bak_file_name)
