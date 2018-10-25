#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Function working with configuration files.
'''
import ConfigParser

import log
import file

def CfgLoadParam(CFGFileName_,Section_,ParamName_):
    '''
    Read param from configuration file.
    @param CFGFileName_: Config file name.
    @param Section_: Section name.
    @param ParamName_: Parameter name.
    @return: Parameter value or None if error.
    '''
    try:
        param=None
        cfg_parser=ConfigParser.ConfigParser()

        cfg_parser.read(CFGFileName_)
        if cfg_parser.has_section(Section_):
            param=cfg_parser.get(Section_,ParamName_)
        return param
    except:
        log.fatal(u'ERROR: read parameter from config file %s : %s : %s.'%(CFGFileName_,Section_,ParamName_))
        return None

def CfgSaveParam(CFGFileName_,Section_,ParamName_,ParamValue_):
    '''
    Write parameter into configuration file.
    @param CFGFileName_: Config file name.
    @param Section_: Section name.
    @param ParamName_: Parameter name.
    @param ParamValue_: Parameter value.
    @return: True/False.
    '''
    try:
        cfg_file=None

        cfg_file_name=file.Split(CFGFileName_)
        path=cfg_file_name[0]
        file_name=cfg_file_name[1]
        if path and (not file.IsDir(path)):
            file.MakeDirs(path)

        if not file.IsFile(CFGFileName_):
            cfg_file=open(CFGFileName_,'w')
            cfg_file.write('')
            cfg_file.close()
            
        cfg_parser=ConfigParser.ConfigParser()
        cfg_file=open(CFGFileName_,'r')
        cfg_parser.readfp(cfg_file)
        cfg_file.close()

        if not cfg_parser.has_section(Section_):
            cfg_parser.add_section(Section_)

        cfg_parser.set(Section_,ParamName_,ParamValue_)

        cfg_file=open(CFGFileName_,'w')
        cfg_parser.write(cfg_file)
        cfg_file.close()
        return True
    except:
        if cfg_file:
            cfg_file.close()
        log.fatal(u'ERROR: write parameter into config file %s.'%(CFGFileName_))
        return False

def CfgDelParam(CFGFileName_,Section_,ParamName_):
    '''
    Delete parameter from configuration file.
    @param CFGFileName_: Config file name.
    @param Section_: Section name.
    @param ParamName_: Parameter name.
    @return: True/False.
    '''
    try:
        cfg_file=None

        if not file.IsFile(CFGFileName_):
            log.icToLog('Configuration file %s not found.'%(CFGFileName_))
            return False
            
        cfg_parser=ConfigParser.ConfigParser()
        cfg_file=open(CFGFileName_,'r')
        cfg_parser.readfp(cfg_file)
        cfg_file.close()

        if not cfg_parser.has_section(Section_):
            return False

        cfg_parser.remove_option(Section_,ParamName_) 

        cfg_file=open(CFGFileName_,'w')
        cfg_parser.write(cfg_file)
        cfg_file.close()

        return True
    except:
        if cfg_file:
            cfg_file.close()
        log.fatal(u'ERROR: delete parameter from config file %s.'%(CFGFileName_))
        return False

def CfgParamCount(CFGFileName_,Section_):
    '''
    Get parameter count in section.
    @param CFGFileName_: Config file name.
    @param Section_: Section name.
    @return: Return parameter count in section or -1 if error.
    '''
    try:
        cfg_file=None

        if not file.IsFile(CFGFileName_):
            log.icToLog('Configuration file %s not found.'%(CFGFileName_))
            return 0
            
        cfg_parser=ConfigParser.ConfigParser()
        cfg_file=open(CFGFileName_,'r')
        cfg_parser.readfp(cfg_file)
        cfg_file.close()

        if not cfg_parser.has_section(Section_):
            return 0

        return len(cfg_parser.options(Section_))
    except:
        if cfg_file:
            cfg_file.close()
        log.fatal()
        return -1

def CfgParamNames(CFGFileName_,Section_):
    '''
    Get names of parameters in section.
    @param CFGFileName_: Config file name.
    @param Section_: Section name.
    @return: Return list of names in section or None if error.
    '''
    try:
        cfg_file=None

        if not file.IsFile(CFGFileName_):
            log.icToLog('Configuration file %s not found.'%(CFGFileName_))
            return None
            
        cfg_parser=ConfigParser.ConfigParser()
        cfg_file=open(CFGFileName_,'r')
        cfg_parser.readfp(cfg_file)
        cfg_file.close()

        if not cfg_parser.has_section(Section_):
            return []

        return cfg_parser.options(Section_)
    except:
        if cfg_file:
            cfg_file.close()
        log.fatal()
        return None
    