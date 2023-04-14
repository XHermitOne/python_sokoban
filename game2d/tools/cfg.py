#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Function working with configuration files.
"""

import os
import os.path
import configparser

from . import log

__version__ = (0, 0, 1, 1)


def loadCfgParam(cfg_filename, section, param_name):
    """
    Read param from configuration file.

    :param cfg_filename: Config file name.
    :param section: Section name.
    :param param_name: Parameter name.
    :return: Parameter value or None if error.
    """
    try:
        param = None
        cfg_parser = configparser.ConfigParser()

        cfg_parser.read(cfg_filename)
        if cfg_parser.has_section(section):
            param = cfg_parser.get(section, param_name)
        return param
    except:
        log.fatal(u'ERROR: read parameter from config file %s : %s : %s.' % (cfg_filename, section, param_name))
        return None


def saveCfgParam(cfg_filename, section, param_name, param_value):
    """
    Write parameter into configuration file.

    :param cfg_filename: Config file name.
    :param section: Section name.
    :param param_name: Parameter name.
    :param param_value: Parameter value.
    :return: True/False.
    """
    cfg_file = None
    try:
        cfg_file_name = os.path.split(cfg_filename)
        path = cfg_file_name[0]
        file_name = cfg_file_name[1]
        if path and (not os.path.isdir(path)):
            os.makedirs(path)

        if not os.path.isfile(cfg_filename):
            cfg_file = open(cfg_filename, 'w')
            cfg_file.write('')
            cfg_file.close()
            
        cfg_parser = configparser.ConfigParser()
        cfg_file = open(cfg_filename, 'r')
        cfg_parser.readfp(cfg_file)
        cfg_file.close()

        if not cfg_parser.has_section(section):
            cfg_parser.add_section(section)

        cfg_parser.set(section, param_name, param_value)

        cfg_file = open(cfg_filename, 'w')
        cfg_parser.write(cfg_file)
        cfg_file.close()
        return True
    except:
        if cfg_file:
            cfg_file.close()
        log.fatal(u'ERROR: write parameter into config file %s.' % cfg_filename)
        return False


def deleteCfgParam(cfg_filename, section, param_name):
    """
    Delete parameter from configuration file.

    :param cfg_filename: Config file name.
    :param section: Section name.
    :param param_name: Parameter name.
    :return: True/False.
    """
    cfg_file = None
    try:
        if not os.path.isfile(cfg_filename):
            log.warning(u'Configuration file %s not found.' % cfg_filename)
            return False
            
        cfg_parser = configparser.ConfigParser()
        cfg_file = open(cfg_filename, 'r')
        cfg_parser.readfp(cfg_file)
        cfg_file.close()

        if not cfg_parser.has_section(section):
            return False

        cfg_parser.remove_option(section, param_name)

        cfg_file = open(cfg_filename, 'w')
        cfg_parser.write(cfg_file)
        cfg_file.close()

        return True
    except:
        if cfg_file:
            cfg_file.close()
        log.fatal(u'ERROR: delete parameter from config file %s.' % cfg_filename)
        return False


def getCfgParamCount(cfg_filename, section):
    """
    Get parameter count in section.

    :param cfg_filename: Config file name.
    :param section: Section name.
    :return: Return parameter count in section or -1 if error.
    """
    cfg_file = None
    try:
        if not os.path.isfile(cfg_filename):
            log.warning('Configuration file %s not found.' % cfg_filename)
            return 0
            
        cfg_parser = configparser.ConfigParser()
        cfg_file = open(cfg_filename, 'r')
        cfg_parser.readfp(cfg_file)
        cfg_file.close()

        if not cfg_parser.has_section(section):
            return 0

        return len(cfg_parser.options(section))
    except:
        if cfg_file:
            cfg_file.close()
        log.fatal()
        return -1


def getCfgParamNames(cfg_filename, section):
    """
    Get names of parameters in section.

    :param cfg_filename: Config file name.
    :param section: Section name.
    :return: Return list of names in section or None if error.
    """
    cfg_file = None
    try:
        if not os.path.isfile(cfg_filename):
            log.warning('Configuration file %s not found.' % cfg_filename)
            return None
            
        cfg_parser = configparser.ConfigParser()
        cfg_file = open(cfg_filename, 'r')
        cfg_parser.readfp(cfg_file)
        cfg_file.close()

        if not cfg_parser.has_section(section):
            return []

        return cfg_parser.options(section)
    except:
        if cfg_file:
            cfg_file.close()
        log.fatal()
        return None
    