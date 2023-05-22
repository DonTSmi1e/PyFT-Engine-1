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