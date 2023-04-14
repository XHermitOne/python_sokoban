# !/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
Utils function.
"""

#--- Imports ---
import time, random, md5
import log

#--- Functions ---
def ReCodeString(String_,StringCP_,NewCP_):
    """
    Encode string from one codepage to another.
    :param String_: String.
    :param StringCP_: String codepage.
    :param NewCP_: New string codepage.
    """
    if NewCP_.upper()=='UNICODE':
        #unicode
        return unicode(String_,StringCP_)

    string=unicode(String_,StringCP_)
    return string.encode(NewCP_)

def SpcDef(Spc_,Struct_):
    """
    Define specification struct of object.

    :type Spc_: C{dictionary}
    :param Spc_: Specification dictinary.
    :type Struct_: C{dictionary}
    :param Struct_: Structure dictionary.
    :rtype: C{dictionary}
    :return: Defined structure dictionary.
    """

    try:
        for key in Spc_.keys():
            if key not in Struct_:
                Struct_[key]=Spc_[key]
    except:
        log.fatal()
    return Struct_

def uuid(*args):
    """
    Generates a universally unique ID.
    Any arguments only create more randomness.
    """
    t=long(time.time()*1000)
    r=long(random.random()*100000000000000000L)

    a=random.random()*100000000000000000L
    data=str(t)+' '+str(r)+' '+str(a)+' '+str(args)
    data=md5.md5(data).hexdigest()
    return data

