"""
    PyFT Engine 1
    Copyright (C) 2023  DonTSmi1e

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    DESCRIPTION: Rendering script. Stores the main logic, displays an image.
"""

import random
import pygame

import logger
import common as c

import pygame_entities as entities

c.r_renderinfo = f"Pygame {pygame.version.ver}, SDL {pygame.version.SDL}"
selected_bg = 0

def Init():
    logger.Print(__name__, "Initializing the video system")

    c.r_objgroups = {"enemy": pygame.sprite.Group(),
                     "global": pygame.sprite.Group()}
    
    c.gamestate_allowed = ["NEWGAME", "GAMEOVER", "INGAME"]
    c.gamestate = "NEWGAME"

    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    pygame.display.set_caption(c.g_name)
    pygame.display.set_icon(entities.sprites["ui"][3])

    c.r_screen = pygame.display.set_mode((c.g_width, c.g_height))
    c.r_clock = pygame.time.Clock()
    c.r_font = pygame.font.Font(None, 15)

    c.r_objgroups["global"].add(entities.Ground(0))
    c.r_objgroups["global"].add(entities.Ground(1))

    if c.r_fullscreen:
        pygame.display.toggle_fullscreen()

    c.r_renderinfo += f" ({pygame.display.get_wm_info()})"

    logger.Print(__name__, "Window created")

def LoadObjects():
    global selected_bg

    selected_bg = random.randint(0, 1)

    c.lvl_score = 0
    c.lvl_ppos = 0
    c.lvl_ypos = {}

    c.r_objgroups["enemy"] = pygame.sprite.Group()

    try:
        c.p_player.kill()
    except:
        pass
    c.p_player = entities.Player()
    c.r_objgroups["global"].add(c.p_player)

    c.r_objgroups["enemy"].add(entities.Pipe(False, 1))
    c.r_objgroups["enemy"].add(entities.Pipe(True, 1))

    c.r_objgroups["enemy"].add(entities.Pipe(False, 3))
    c.r_objgroups["enemy"].add(entities.Pipe(True, 3))

    c.r_objgroups["enemy"].add(entities.Pipe(False, 5))
    c.r_objgroups["enemy"].add(entities.Pipe(True, 5))

def Shutdown():
    pygame.quit()
    logger.Print(__name__, "The video system is disabled.")

def Update():
    global selected_bg

    c.r_clock.tick(c.r_fps)
    c.r_screen.fill((0,0,0))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            Shutdown()
            return 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAUSE:
                c.r_pause = not c.r_pause
                
            if c.gamestate in ["NEWGAME", "GAMEOVER"]:
                if event.key == pygame.K_UP:
                    c.gamestate = "INGAME"
                    LoadObjects()
                    c.p_player.jump()
            elif c.gamestate == "INGAME":
                if event.key == pygame.K_UP:
                    c.p_player.jump()
    
    if c.r_pause:
        return

    c.r_screen.blit(entities.sprites["background"][selected_bg], (0, 0))

    for group in c.r_objgroups:
        c.r_objgroups[group].update()
        c.r_objgroups[group].draw(c.r_screen)

    # HUD code
    hud_score = str(c.lvl_score)
    if len(hud_score) == 1:
        c.r_screen.blit(entities.sprites["hud"][int(hud_score)], ((c.g_width/2)-14,40))
    elif len(hud_score) == 2:
        c.r_screen.blit(entities.sprites["hud"][int(hud_score[0])], ((c.g_width/2)-25,40))
        c.r_screen.blit(entities.sprites["hud"][int(hud_score[1])], ((c.g_width/2)-3,40))
    elif len(hud_score) == 3:
        c.r_screen.blit(entities.sprites["hud"][int(hud_score[0])], ((c.g_width/2)-36,40))
        c.r_screen.blit(entities.sprites["hud"][int(hud_score[1])], ((c.g_width/2)-14,40))
        c.r_screen.blit(entities.sprites["hud"][int(hud_score[2])], ((c.g_width/2)+8,40))

    if c.gamestate == "NEWGAME":
        c.r_screen.blit(entities.sprites["ui"][0], (0,0))
    elif c.gamestate == "GAMEOVER":
        c.r_screen.blit(entities.sprites["ui"][1 if c.lvl_score < 1000 else 2], (0,0))

    if c.g_debug:
        debug = [c.r_font.render(f"PyFT Engine 1", True, (255, 255, 255)),
                c.r_font.render(f"FPS: {c.r_fps}", True, (255, 255, 255)),
                c.r_font.render(f"Game state: {c.gamestate}", True, (255, 255, 255)),
                c.r_font.render(f"Current time: {logger.datetime.now().strftime('%H:%M:%S')}", True, (255, 255 ,255)),
                c.r_font.render(f"Warnings: {logger.warnings}", True, (255, 255, 0)),
                c.r_font.render(f"Errors: {logger.errors}", True, (255, 0, 0))]
        RenderLines(debug, 10)

    pygame.display.flip()

def RenderLines(lines, firstpos):
    firstpos = 10
    for line in lines:
        line.set_alpha(200)
        c.r_screen.blit(line, (10, firstpos+20))
        firstpos += 20