# !/usr/bin/env python
#  -*- coding: utf-8 -*-
'''
Resource file functions.
'''

#--- Imports ---
import cPickle

import txt
import log
import file
#--- Constants ---
#--- Specifications ---
#--- Functions ---
def LoadResource(FileName_):
    '''
    Load resource file.
    @param FileName_: Resource file name.
    '''
    #Pickle?
    struct=LoadResourcePickle(FileName_)
    if struct is None:
        #No pickle. Is text.
        struct=LoadResourceText(FileName_)
    if struct is None:
        #Read error
        log.PrintLog('ERROR: Resource file format %s.'%(FileName_))
        return None
    return struct
    
    
def LoadResourcePickle(FileName_):
    '''
    Load pickle resource file.
    @param FileName_: Resource file name.
    '''
    if file.IsFile(FileName_):
        try:
            f=open(FileName_)
            struct=cPickle.load(f)
            f.close()
            return struct
        except:
            log.fatal(u'ERROR: Read resource file %s.'%(FileName_))
            return None
    else:
        log.PrintLog('ERROR: File %s not found.'%(FileName_))
        return None

def LoadResourceText(FileName_):
    '''
    Load text resource file.
    @param FileName_: Resource file name.
    '''
    if file.IsFile(FileName_):
        try:
            f=open(FileName_)
            txt=f.read().replace('\r\n','\n')
            f.close()
            return eval(txt)
        except:
            log.PrintLog('ERROR: Read resource file %s.'%(FileName_))
            return None
    else:
        log.PrintLog('ERROR: File %s not found.'%(FileName_))
        return None

def SaveResourcePickle(FileName_,Resource_):
    '''
    Save pickle resource file.
    @param FileName_: Resource file name.
    @Resource_: Resource data.
    @return: True/False.
    '''
    try:
        dir_name=file.DirName(FileName_)
        CreateInitFile(dir_name)

        f=open(FileName_, 'w')
        cPickle.dump(Resource_,f)
        f.close()
        log.PrintLog('Resource file %s saved in pickle format.'%(FileName_))
        return True
    except:
        log.PrintLog('ERROR: Save resource file %s in pickle format.'%(FileName_))
        return False

def SaveResourceText(FileName_,Resource_):
    '''
    Save text resource file.
    @param FileName_: Resource file name.
    @Resource_: Resource data.
    @return: True/False.
    '''
    try:
        dir_name=file.DirName(FileName_)
        CreateInitFile(dir_name)

        f=open(FileName_,'w')
        text=txt.StructToTxt(Resource_)
        f.write(text)
        f.close()
        log.PrintLog('Resource file %s saved in text format.'%(FileName_))
        return True
    except:
        log.PrintLog('ERROR: Save resource fiel %s in text format.'%(FileName_))
        return False
