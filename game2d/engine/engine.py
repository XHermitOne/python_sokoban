#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Game engine module.
"""

# --- Imports ---
import time
import pygame
# import pygame.locals

from . import scene
from . import map2d

from ..tools import cfg

__version__ = (0, 0, 3, 1)

ENGINE_DELAY = 0.05


# --- Functions ---
def sokobanEngine():
    """
    Sokoban engine main function.
    """
    # ~~~ Init block ~~~
    # Scene creation
    game_scene = scene.sokobanScene()
    game_scene.SetImgDir(cfg.loadCfgParam('game2d.cfg', 'SOKOBAN', 'img_dir'))
    # Init
    game_scene.Init()

    # Font
    game_scene.SetFont('font.ttf')

    # Title
    game_scene.TitlePage()

    # Map create
    game_map = map2d.sokobanMap()
    game_map.SetMapDir(cfg.loadCfgParam('game2d.cfg', 'SOKOBAN', 'map_dir'))
    # Load first level
    game_map.LoadLevel(int(cfg.loadCfgParam('game2d.cfg', 'SOKOBAN', 'cur_level')))
    game_map.SetScene(game_scene)
    
    # Game over flag
    is_game_over = False
    is_win = False
    # Main loop
    while not (is_game_over or is_win):
        # Create all objects
        game_scene.Clear()
        game_scene.CreateObjects(game_map)
        game_hero = game_scene.GetHero()

        # Center
        game_map.Center()
        # Show scene
        # game_scene.DrawBackground()
        game_scene.DrawDecor()
        
        info_txt = u'SOKOBAN Level: %d' % game_map.GetLevel()
        pygame.display.set_caption(info_txt)
        game_scene.DrawTextXY(info_txt, 5, 5, (224, 192, 128))
    
        game_scene.RefreshScreen()
        game_scene.Draw()
        
        # Event loop
        run = True
        break_level = False
        while run:
            # get input
            for event in pygame.event.get():
                # Quit
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F10):
                    run = False
                    is_game_over = True

                # Break level
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    run = False
                    break_level = True
                    break

                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    game_hero.RunToRight()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    game_hero.RunToLeft()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    game_hero.RunToUp()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    game_hero.RunToDown()

            # End level
            if sokobanWinLevel(game_scene):
                run = False

        # Load next level
        if not break_level:
            is_win = not game_map.LoadNext()
        else:
            game_map.LoadCur()
            
        # pygame.display.set_caption('SOKOBAN Level: %d'%(game_map.GetLevel()))
        game_scene.DrawTextXY(u'SOKOBAN Level: %d' % (game_map.GetLevel()), 5, 5)

        if is_win and (not is_game_over):
            game_scene.BacksidePage()

    # Save state
    cfg.saveCfgParam('game2d.cfg', 'SOKOBAN', 'cur_level', game_map.GetLevel() - 1)


def sokobanWinLevel(Scene_):
    """
    Win?
    :param Scene_: Scene object.
    :return: True/False.
    """
    for box in Scene_.GetThings():
        if box.GetGround() != map2d.MAP_PLACE:
            return False
    return True
