# !/usr/bin/env python
#  -*- coding: utf-8 -*-
'''
File working functions.
'''

#--- Imports ---
import os
import os.path
import shutil 
import sys

# from shutil import copytree as CopyFile
from os import rename as Rename
from os import makedirs as MakeDirs
from os import getcwd as GetCurDir
from os import remove as Remove
from os import unlink as UnLink
from os import listdir as ListDir

from os.path import isfile as IsFile
from os.path import isdir as IsDir
from os.path import split as Split
from os.path import splitext as SplitExt
from os.path import dirname as DirName
from os.path import basename as BaseName
from os.path import abspath as AbsPath
from os.path import walk as Walk
from os.path import join as Join

from sys import path as PATH
from sys import argv as ARGV

import log

#--- Functions ---
def RelativePath(Path_):
    '''
    Get relative path.
    @param Path_: Path.
    '''
    if not Path_:
        return Path_
    #ATTENTION!!! All sleshes UNIX type!
    cur_work_dir=os.getcwd().replace('\\', '/').lower()
    Path_=Path_.replace('\\','/').lower()
    return Path_.replace(cur_work_dir,'.')

def AbsolutePath(Path_):
    '''
    Get absolute path.
    @param Path_: Path.
    '''
    if not Path_:
        return Path_
    cur_work_dir=os.getcwd().replace('\\', '/').lower()
    Path_=Path_.replace('\\','/').lower()
    return Path_.replace('./', cur_work_dir+'/')

def CopyFile(SrcFileName_, DstFileName_):
    '''
    Copy file with path.
    '''
    if IsFile(SrcFileName_):
        dst_path=DirName(DstFileName_)
        if not IsDir(dst_path):
            MakeDirs(dst_path)
        shutil.copyfile(SrcFileName_,DstFileName_)
        return True
    return False

def CreateBAKFile(FileName_):
    '''
    Create baackup *.bak file.
    @param FileName_: File name.
    '''
    bak_file_name=FileName_+'.bak'
    CopyFile(FileName_, bak_file_name)
