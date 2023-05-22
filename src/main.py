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

    DESCRIPTION: Main script. Calls render and console functions.
"""

import sys
import threading

import logger

import common as c

running = True
render_disabled = False

index = 0
for arg in sys.argv:
    match arg:
        case "-debug":
            c.g_debug = True
        case "-mode":
            c.r_rendermode = int(sys.argv[index+1])
            index += 1
        case "-fullscreen":
            #c.r_fullscreen = True
            pass
    index += 1

match c.r_rendermode:
    #case -1:
    #    import template_render as render
    case 1:
        import pygame_render as render
    case 2:
        # import pysdl_render as render
        logger.Print(__name__, "PySDL not supported yet", "ERROR")
        sys.exit(0)
    case _:
        logger.Print(__name__, "Invalid r_rendermode", "ERROR")
        sys.exit(0)

print("""    PyFT Engine 1  Copyright (C) 2023  DonTSmi1e
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions.""")

if c.g_debug:
    def console_update(line: str):
        global running, render_disabled
        line = line.split(" ")
        match line[0].lower():
            case "r_list":
                index = 0
                for group in c.r_objgroups:
                    logger.Print(__name__, "Group: " + group)
                    for object in c.r_objgroups[group]:
                        logger.Print(__name__, f"[{index}] {object}")
                        index += 1
            case "r_remove":
                del_index = int(line[1])
                index = 0
                done = False
                for group in c.r_objgroups:
                    if not done:
                        for object in c.r_objgroups[group]:
                            if index == del_index:
                                object.kill()
                                done = True
                                break
                            index += 1
                    else:
                        logger.Print("Console", "Done")
                        break
            case "r_gamestate":
                c.gamestate = line[1]
                logger.Print("Console", f"Current gamestate: {c.gamestate}")
            case "r_renderinfo":
                logger.Print(__name__, c.r_renderinfo)
            case "r_restart":
                render.LoadObjects()
                logger.Print("Console", f"Level reloaded")
            case "r_fpsmax":
                c.r_fps = int(line[1])
                logger.Print("Console", f"Max FPS: {c.r_fps}")
            case "lvl_score":
                c.lvl_score = int(line[1])
                logger.Print("Console", f"Current score: {c.lvl_score}")
            case "p_noclip":
                c.p_noclip = not c.p_noclip
                logger.Print("Console", f"Noclip: {c.p_noclip}")
            case "rendertoggle":
                render_disabled = not render_disabled
                logger.Print("Console", f"Render: {render_disabled}")
            case "help":
                logger.Print("Console", c.c_help)
            case _:
                logger.Print("Console", f"{line[0].lower()} - Unknown command. Type 'help' to display a list of all commands.")

    def console():
        logger.Print("Console", "Console enabled")
        while running:
            line = input()
            try:
                console_update(line)
            except IndexError:
                logger.Print("Console", "Not enough arguments")
            except Exception as ex:
                logger.Print("Console", ex)

    console_thread = threading.Thread(target=console)
    console_thread.daemon = True
    console_thread.start()

if __name__ == "__main__":
    render.Init()

    if c.g_debug and not c.msg_invalidgamestate:
        c.msg_debugmode = True
        logger.Print(__name__, "Debug mode enabled.", "DEBUG")

    logger.Print(__name__, "Main loop started")

    while running:
        if c.gamestate not in c.gamestate_allowed and not c.msg_invalidgamestate:
            c.msg_invalidgamestate = True
            logger.Print(__name__, "Noticed that the current game state is not in the allowed list. Keep in mind.", "WARN")
        elif c.gamestate in c.gamestate_allowed and c.msg_invalidgamestate:
            c.msg_invalidgamestate = False

        if not render_disabled:
            update = render.Update()

        if update == 0:
            running = False

    logger.Print(__name__, "Loop has been completed")

    sys.exit(0)
    