from oein import *
from screens.InGame import (
    insertDamage,
    gameLandWidth,
    gameLandHeight,
    borderDX,
    borderDY,
    isPlayerInside,
)


class EntityBone(Screen):
    type: bool = False
    img: pygame.Surface

    def __init__(self, screen, type=False, rotate: int = 0):
        super().__init__(screen)
        self.type = type
        fname = ""
        if type:
            fname = "_blue"
        self.img = pygame.image.load(f"images/bone/vbone{fname}.png")
        self.img = pygame.transform.rotate(self.img, rotate)

    def build(self, x: int, y: int, height: int):
        wid = 16
        hei = height
        if x < 0:
            return
        if x > gameLandWidth:
            return
        stx = x + borderDX + int(Constants["centerx"] - gameLandWidth / 2 + 5)
        sty = y + borderDY + yflex(1, 2) + 5
        if y + hei > gameLandHeight - 10:
            hei = gameLandHeight - y - 10
        if hei < 0:
            hei = 0
        self.screen.blit(
            pygame.transform.scale(self.img, (32, hei)),
            (
                stx,
                sty,
            ),
        )

        if isPlayerInside(x, y, wid, hei):
            insertDamage(1)
