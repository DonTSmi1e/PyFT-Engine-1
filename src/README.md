# PyFT Engine 1
![](https://www.gnu.org/graphics/gplv3-with-text-136x68.png)

## Source files

| File          | Description                                         |
|---------------|-----------------------------------------------------|
| common.py     | Stores variables used by multiple scripts.          |
| logger.py     | Engine controlled logger.                           |
| *_render.py   | The script responsible for rendering.               |
| *_entities.py | Stores the entities used by *_render.py             |
| main.py       | Main script. Manipulates the entire engine at once. |

## How does the game start
* **main.py**
    * Import of shared variables
    * Argument Handling
    * Import render script
        * Handling the *c.r_rendermode* variable
        * Regarding its value, import **_render.py* module as *render*
    * If debug mode is enabled, enable the console.
    * `render.Init()` - Initialize the render script.
    * In a loop: `render.Update()` - Perform rendering
* ***_render.py**
    * `Init()` - Creating a window, setting the required values ​​of variables
    * `LoadObjects()` - Recreate the player object, reset the level and restart.
    * `Shutdown()` - Disable rendering.
    * `Update()` - Perform window rendering.
        * Handling *c.r_gamestate*
            * Performing an action based on this.

## How to create your own image rendering script
First, you need a template:
```py
"""template_render.py"""

# import <your rendering library>

import logger
import common as c

c.r_renderinfo = "Render info"

def Init():
    c.r_objgroups = {"global": []}
    c.gamestate_allowed = ["NEWGAME", "GAMEOVER", "INGAME"]
    c.gamestate = "NEWGAME"

    logger.Print(__name__, "Init()")

def LoadObjects():
    logger.Print(__name__, "LoadObjects()")

def Shutdown():
    logger.Print(__name__, "Shutdown()")

def Update():
    pass
```
In the `Init()` function - initialize your library, be sure to set the *c.r_objgroups*, *c.gamestate_allowed*, *c.gamestate* variables

In the `LoadObjects()` function, write the code to completely reload the level. Recreate the player object, clear the groups, fill them with new objects.

In the `Shutdown()` function, safely shut down YOUR LIBRARY, not the entire program.

In the `Update()` function, draw everything that happens to the window.

Feel free to go into *pygame_render.py* and *pygame_entities.py* to understand the rendering logic.
