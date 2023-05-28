from oein import *
import obb
from screens.InGame import (
    getPlayerXY,
    insertDamage,
    playerDamagedInThisFrame,
    playerSize,
)


# Shoot after 0.5 sec
class EntityGasterBlaster(Screen):
    imgs: list[pygame.Surface] = []

    endX: int
    endY: int
    endRot: int

    frame: int = 0
    height = 96

    x: int = Constants["centerx"] - 48
    y: int = 0

    def __init__(self, screen, x: int, y: int, rotation: int = 0):
        super().__init__(screen)
        self.endX = x
        self.endY = y
        self.endRot = rotation
        self.rot = 0
        for i in range(5):
            self.imgs.append(
                pygame.transform.scale2x(
                    pygame.image.load(f"images/GasterBlaster/{i}.png")
                )
            )

        self.rotate(0)

    def rotate(self, rot: int, opacity: float = 1):
        opacity = min(opacity, 1)
        w = Constants["screenx"] * 2
        h = self.height

        surfacea = pygame.Surface((w, h))
        surfacea.set_colorkey(Color["BLACK"])
        surfacea.fill(Color["WHITE"])
        surfacea.set_alpha(int(opacity * 255))
        img = surfacea.copy()
        img.set_colorkey(Color["BLACK"])
        rect = img.get_rect()
        rect.center = (self.x + int(h / 2), self.y + int(h / 2))
        old_ce = rect.center
        nimg = pygame.transform.rotate(surfacea, rot - 90)
        rec = nimg.get_rect()
        rec.center = old_ce
        self.rec = rec
        self.nim = nimg

    def getImg(self):
        img = self.imgs[min(int(self.frame / (sec2frame(0.5) / 4)), 4)]
        img = pygame.transform.rotate(img, self.rot - 90)
        return img

    def build(self):
        if self.frame < sec2frame(0.7):
            self.x = min(int(self.endX / sec2frame(0.3) * self.frame), self.endX)
            self.y = min(int(self.endY / sec2frame(0.3) * self.frame), self.endY)
            self.rot = min(
                int((self.endRot + 90) / sec2frame(0.3) * self.frame - 90), self.endRot
            )

            self.rotate(self.rot, self.frame / sec2frame(0.7))

            if self.frame > sec2frame(0.4):
                self.screen.blit(
                    self.nim,
                    self.rec,
                )
            self.screen.blit(self.getImg(), (self.x, self.y))
        else:
            if self.frame <= sec2frame(0.7):
                self.rotate(self.rot, self.frame / sec2frame(0.7))
            self.screen.blit(
                self.nim,
                self.rec,
            )
            self.screen.blit(self.getImg(), (self.x, self.y))

            if playerDamagedInThisFrame:
                return

            playerXY = getPlayerXY()
            playerXY = (playerXY[0] + playerSize / 2, playerXY[1] + playerSize / 2)

            points = obb.rec2points(
                self.x + int(self.height / 2),
                self.y + int(self.height / 2),
                Constants["screenx"] * 2,
                96,
                self.rot - 90,
            )
            if obb.OBB(
                points,
                obb.Point(playerXY),
            ):
                insertDamage(1, False)

        self.frame += 1
