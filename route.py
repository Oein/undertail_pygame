import screens.MainScreen as MainScreen
import screens.InGame as InGameScreen
import screens.SureToExit as SureToExit
import screens.PauseScreen as PausedScreen
import screens.SureToGoToMain as SureToGoToMainScreen
import screens.dead as DeadScreen
from pygame import Surface
from typing import Dict
from oein import Screen

path = "/"
pathQueue = ["/"]
routes: Dict[str, Screen] = {}


def initRoutes(screen: Surface):
    routes["/"] = MainScreen.MainScreen(screen)
    routes["/inGame"] = InGameScreen.InGameScreen(screen)
    routes["/sureToExit"] = SureToExit.SureToExit(screen)
    routes["/sureToMain"] = SureToGoToMainScreen.SureToGoToMain(screen)
    routes["/pause"] = PausedScreen.PauseScreen(screen)
    routes["/dead"] = DeadScreen.DeadScreen(screen)


def push(lopath: str):
    global path
    if path != lopath:
        pathQueue.append(lopath)
        path = lopath


def to(lopath: str):
    global path
    global pathQueue
    if path != lopath:
        pathQueue = [lopath]
        path = lopath


def back():
    global path
    global pathQueue

    if len(pathQueue) != 1:
        del pathQueue[-1]
        path = pathQueue[-1]
