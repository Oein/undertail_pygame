from oein import *
import obb
from screens.InGame import (
    getPlayerXY,
    insertDamage,
    getPlayerDamagedInThisFrame,
    getPlayerSize,
)

# 0 (MovStart)
# 0.366 (MovEnd)
# 0.699 (AniStart)
# 0.799 (AniEnd & Lazer)
# 0.983 (GoOutStart)
# 1.366 (LazerEnd, GoOutEnd)


def ignoreZero(num: float):
    if num == 0:
        return 0.01
    return num


dx = [0, -200, 0, Constants["screenx"]]
dy = [-200, 0, Constants["screeny"], 0]


def getSpawnTimeByShoot(shootFrame: float):
    return round(shootFrame - sec2frame(0.799))


rotMap = [{}, {}, {}, {}, {}]


# Shoot after 0.5 sec
class EntityGasterBlaster(Screen):
    imgs: list[pygame.Surface] = []

    shootHeight: int = 0

    endX: int
    endY: int
    endRot: int

    frame: int = 0
    height = 96

    x: int = Constants["centerx"] - 48
    y: int = 0

    opacity: float = 0

    animaiting = False
    aniStartFrame: int = 0
    aniEndFrame: int = 0

    aniStartX: int = 0
    aniStartY: int = 0
    aniStartR: int = 0
    aniStartO: int = 1

    aniDiffX: float = 0
    aniDiffY: float = 0
    aniDiffR: float = 0
    aniDiffO: float = 0

    def __init__(
        self,
        screen,
        x: int,
        y: int,
        rotation: int = 0,
        shootHeight: int = round(getPlayerSize() * 2.5),
    ):
        super().__init__(screen)
        self.endX = x
        self.endY = y
        self.endRot = rotation
        self.shootHeight = shootHeight
        self.rot = 0
        for i in range(5):
            self.imgs.append(
                pygame.transform.scale2x(
                    pygame.image.load(f"images/GasterBlaster/{i}.png")
                )
            )

        self.rotate(rotation + 180)
        self.animate(x, y, rotation, 0, sec2frame(0.366))

    def rotate(self, rot: int, opacity: float = 1):
        opacity = min(opacity, 1)
        w = Constants["screenx"] * 2.5
        h = self.shootHeight

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
        idx = max(
            min(
                round(
                    4
                    * max(ignoreZero(self.frame - sec2frame(0.699)), 0.001)
                    / sec2frame(0.1)
                ),
                4,
            ),
            0,
        )
        imgItem = rotMap[idx].get(self.rot - 90)
        if imgItem is not None:
            return imgItem
        img = self.imgs[idx]
        img = pygame.transform.rotate(img, self.rot - 90)
        rotMap[idx][self.rot - 90] = img
        return img

    def animate(self, endX: int, endY: int, endRot: int, opacity: float, frame: int):
        self.aniStartFrame = self.frame
        self.aniEndFrame = self.frame + frame

        self.aniStartX = self.x
        self.aniStartY = self.y
        self.aniStartR = self.rot
        self.aniStartO = self.opacity

        self.aniDiffX = (endX - self.x) / frame
        self.aniDiffY = (endY - self.y) / frame
        self.aniDiffR = (endRot - self.rot) / frame
        self.aniDiffO = (opacity - self.opacity) / frame

        self.animaiting = True

    def calculateAnimation(self):
        if not (self.animaiting):
            return

        self.x = round(
            self.aniStartX + self.aniDiffX * (self.frame - self.aniStartFrame)
        )
        self.y = round(
            self.aniStartY + self.aniDiffY * (self.frame - self.aniStartFrame)
        )
        self.rot = round(
            self.aniStartR + self.aniDiffR * (self.frame - self.aniStartFrame)
        )
        self.opacity = self.aniStartO + self.aniDiffO * (
            self.frame - self.aniStartFrame
        )
        self.rotate(self.rot, self.opacity)

        if self.frame >= self.aniEndFrame:
            self.animaiting = False

    def build(self):
        self.calculateAnimation()

        if self.frame == sec2frame(0.700):
            self.animate(self.x, self.y, self.rot, 1, sec2frame(0.810 - 0.720))
        if self.frame == sec2frame(0.983):
            newX = self.x
            newY = self.y

            differer = max(self.x, self.y) + 200
            difMaxer = (
                max(
                    abs(Constants["screenx"] - self.x),
                    abs(Constants["screeny"] - self.y),
                )
                + 200
            )

            if self.rot == 0:
                newY = -200
            if self.rot == 90:
                newX = -200
            if self.rot == 180:
                newY = Constants["screeny"] + 200
            if self.rot == 270:
                newX = Constants["screenx"] + 200
            if self.rot == 45:
                newX = newX - differer
                newY = newY - differer
            if self.rot == 135:
                newX = newX - difMaxer
                newY = newY + difMaxer
            if self.rot == 225:
                newX = newX + difMaxer
                newY = newY + difMaxer
            if self.rot == 315:
                newX = newX + differer
                newY = newY - differer

            self.animate(newX, newY, self.rot, 0.2, sec2frame(1.366 - 0.983))
        if self.frame == sec2frame(1.366):
            self.animate(self.x, self.y, self.rot, 0, sec2frame(0.1))

        self.screen.blit(
            self.nim,
            self.rec,
        )
        self.screen.blit(self.getImg(), (self.x, self.y))

        if not getPlayerDamagedInThisFrame() and sec2frame(
            0.810
        ) <= self.frame <= sec2frame(1.15):
            playerXY = getPlayerXY()
            playerXY = (
                playerXY[0] + getPlayerSize() / 2,
                playerXY[1] + getPlayerSize() / 2,
            )

            points = obb.rec2points(
                self.x + int(self.height / 2),
                self.y + int(self.height / 2),
                Constants["screenx"] * 2.5,
                96,
                self.rot - 90,
            )
            if obb.OBB(
                points,
                obb.Point(playerXY),
            ):
                insertDamage(1, False)

        self.frame += 1
