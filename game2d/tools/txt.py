# !/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
Text and string functions.
"""

#--- Imports ---
import log
#--- Functions ---
#Text padding
PADDING='    '

def StructToTxt(Struct_, Level_=0):
    """
    Convert dict-list struct to text.
    :param Struct_ : Dict-list struct.
    :param Level_: Cur level.
    """
    try:
        txt=''
        obj_type=type(Struct_)
        if obj_type==ListType:
            txt=txt+'\n'+Level_*PADDING+'[\n'
            for obj in Struct_:
                txt+=Level_*PADDING
                txt+=StructToTxt(obj, Level_+1)
                txt+=',\n'
            if len(Struct_)<>0:
                txt=txt[:-2]
            txt=txt+'\n'+Level_*PADDING+']\n'
        elif obj_type==DictType:
            txt=txt+'\n'+Level_*PADDING+'{\n'
            keys=Struct_.keys()
            values=Struct_.values()
            for key in keys:
                txt=txt+Level_*PADDING+'\''+key+'\':'
                txt+=StructToTxt(Struct_[key], Level_+1)
                txt+=',\n'
            if len(keys)<>0:
                txt=txt[:-2]
            txt=txt+'\n'+Level_*PADDING+'}\n'
        elif obj_type==StringType:
            txt=txt+'\''+Struct_.replace('\'','\\\'').replace('\"','\\\"').replace('\r','\\r').replace('\n','\\n').replace('\t','\\t')+'\''
        elif obj_type==UnicodeType:
            txt=txt+'\''+Struct_.encode('CP1251').replace('\'','\\\'').replace('\"','\\\"').replace('\r','\\r').replace('\n','\\n').replace('\t','\\t')+'\''
        else:
            txt=txt+str(Struct_)
        
        return txt
    except:
        log.fatal(u'ERROR: Level %d: '%(Level_))
