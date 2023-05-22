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

    DESCRIPTION: Shared variables used by multiple scripts.
"""

# Render variables  ---
r_renderinfo = "Not initialized"
r_rendermode = 1            # 1 - Pygame; 2 - PySDL
r_objgroups = None          # Should be None, later render.py will set this variable to the sprite dictionary.
r_pause = False             # If True, rendering will be paused.
r_fps = 75                  # Max framerate.
r_fullscreen = False        # % for the future % # Toggles fullscreen mode
r_screen = None
r_clock = None
r_font = None

# Player variables  ---
p_player = None             # Will be used to store the player's sprite.
p_noclip = False            # Cheating function. Turns off pipe collision.
p_angle_max = 45            # Player max angle (positive)
p_angle_min_ph1 = -45
p_angle_min_ph2 = -90       # Player min angle (negative)       

# Level variables   ---
lvl_speed = 1               # Responsible for the speed of movement of the ground and pipes. Resets to 1 every level reload.
lvl_score = 0               # Player's score. According to the script, the game will behave inappropriately after 999. CANNOT BE NEGATIVE
lvl_velocity = 1.5          # "Bird jump power"
lvl_ppos = 0                # Pipe position relative to other pipes
lvl_ypos = {}               # Pipe position in Y

# Gamestate         ---
gamestate_allowed = None    # There should be a list of allowed states here. This is necessary so that the game does not perform unnecessary actions if the state is incorrect.
gamestate = None            # The current state of the game.

# Engine settings   ---
g_version = "22.05.2023"    # Engine version
g_name = "Flappy Thing"     # Window name
g_debug = False             # Debug mode
g_width = 288               # Window width
g_height = 512              # Window height

# Debug console     ---
c_help = """List of all commands:
r_list - List of all active objects
r_remove <index> - Remove object by index
r_gamestate <gamestate> - Change gamestate
r_renderinfo - Show render information
r_restart - LoadObjects()
r_fpsmax <fps> - Set max FPS
lvl_score <score> - Set score
p_noclip - Toggle noclip
rendertoggle - Toggle rendering (will freeze window)
help - Shows this message
"""

# Message states    ---     # If False: The message has not been shown yet; If True: The message is shown.
msg_invalidgamestate = False
msg_debugmode = False
