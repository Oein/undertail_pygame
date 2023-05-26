import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame
import route
from common import *
import common
from oein import *

# pygame setup
pygame.init()


route.initRoutes(screen)

clock = pygame.time.Clock()

pygame.mixer.init()

while common.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            route.push("/sureToExit")
        if event.type == pygame.KEYDOWN:
            kv = KeyEvent(
                text=event.__dict__["unicode"],
                keyCode=event.__dict__["key"],
                mod=event.__dict__["mod"],
                scancode=event.__dict__["scancode"],
                type=pygame.KEYDOWN,
            )
            route.routes[route.path].onKeyDown(kv)
        if event.type == pygame.KEYUP:
            kv = KeyEvent(
                text=event.__dict__["unicode"],
                keyCode=event.__dict__["key"],
                mod=event.__dict__["mod"],
                scancode=event.__dict__["scancode"],
                type=pygame.KEYDOWN,
            )
            route.routes[route.path].onKeyUp(kv)

    route.routes[route.path].build()
    route.routes[route.path].superBuild()

    pygame.display.flip()
    clock.tick(Constants["framerate"])

pygame.quit()
