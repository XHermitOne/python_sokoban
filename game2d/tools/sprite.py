#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Abstract sprite class.
'''

#--- Imports ---
import os

import pygame
from pygame.locals import *

#--- Constants ---

#--- Classes ---
class mySprite(pygame.sprite.Sprite):

    def __init__(self,ImageFiles_=None,SoundFiles_=None):
        '''
        Constructor.
        @param ImageFiles_: Image file name list.
        @param SoundFiles_: Sound file name list.
        '''
        pygame.sprite.Sprite.__init__(self)

        #Image list
        self.images=[]
        #Load images
        if ImageFiles_:
            self.LoadImages(*tuple(ImageFiles_))

        self.GraphInit()

    def GraphInit(self):
        '''
        Init graph attributes.
        '''
        if self.images<>[]:
            self.image=self.images[0]
            self.rect=self.image.get_rect() #Sprite rect

    def LoadImage(self,ImageFile_):
        '''
        Load image.
        '''
        file=os.getcwd()+'//img//'+ImageFile_
        try:
            surface=pygame.image.load(file)
        except pygame.error:
            raise SystemExit, 'ERROR: Load image \'%s\' %s'%(file,pygame.get_error())
        return surface.convert()

    def LoadImages(self,*ImageFiles_):
        '''
        Load images.
        '''
        for file in ImageFiles_:
            self.images.append(self.LoadImage(file))
        return self.images

    def update(self):
        '''
        Update sprite.
        '''
        pass
