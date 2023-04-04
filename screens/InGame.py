from oein import *
from events.upDownBone import *
from events.die import *
from components.InGame.button import *

frame = 0
maxHP = 100
hp = 100
maxKR = 92
kr = 92
isMyTurn = False

gameLandWidth = 200
gameLandHeight = 200
borderDX = 0
borderDY = 0

playerSize = gameLandHeight / 9
playerSpeed = 3

gravity = 7
gravityDX = [0, gravity, -1 * gravity, 0, 0]
gravityDY = [0, 0, 0, gravity, -1 * gravity]
gravityDir = 0

cannotMove = False

attackSound: pygame.mixer.Sound
damagedSound: pygame.mixer.Sound
dingSound: pygame.mixer.Sound
playerDamagedInThisFrame = False

playerX = 0
playerY = 0


def setGravity(gravity_: int):
    global gravityDX
    global gravityDY
    global gravity
    gravity = gravity_
    gravityDX = [0, gravity, -1 * gravity, 0, 0]
    gravityDY = [0, 0, 0, gravity, -1 * gravity]


def playAttackSound():
    attackSound.play()


def gmaeLandXY():
    return (
        int(Constants["centerx"] - gameLandWidth / 2) + borderDX,
        yflex(1, 2) + borderDY,
    )


def insertDamage(dmg: int, forced=False):
    global hp
    global kr
    global playerDamagedInThisFrame

    if forced == False and playerDamagedInThisFrame:
        return

    damagedSound.play()
    playerDamagedInThisFrame = True
    hp = round(hp - dmg)
    kr = round(kr - dmg)

    if hp <= 0 and kr >= 1:
        hp = 1

    if hp == 0:
        die()
        return


def isPlayerInside(x: int, y: int, width: int, height: int):
    return x + width >= playerX >= x and y + height >= playerY >= y


class ComponentSans(Screen):
    sansImages: list[pygame.Surface]
    sansEndX: int
    sansStartY: int = yflex(1, 6)
    frame: int = 0
    saying: bool = False
    gonnaSay: str = ""
    saied: str = ""
    sayingFrame: int = 0
    boSay: bool = False
    sansSpeakSound: pygame.mixer.Sound

    def __init__(self, screen):
        self.sansImages = []
        for i in range(1, 19, 1):
            self.sansImages.append(pygame.image.load(f"images/sans/sans{i}.png"))
            self.sansImages[i - 1] = pygame.transform.scale(
                self.sansImages[i - 1], (200, 200)
            )
        self.sansEndX = Constants["centerx"] + 100
        self.frame = 0
        self.sansSpeakSound = pygame.mixer.Sound("audio/SansSpeak.ogg")
        super().__init__(screen)

    def say(self, str: str):
        if self.saying:
            return
        self.saied = ""
        self.gonnaSay = str
        self.saying = True
        self.sayingFrame = 0
        self.boSay = False

    def boldSay(self, str: str):
        if self.saying:
            return
        self.saied = ""
        self.gonnaSay = str
        self.saying = True
        self.sayingFrame = 0
        self.boSay = True
        self.sansImages = [
            pygame.transform.scale(
                pygame.image.load("images/sans/noeye.png"), (200, 200)
            )
        ]
        self.frame = 0

    def build(self):
        speed = 10
        self.frame += 1
        self.frame %= len(self.sansImages) * speed
        self.screen.blit(
            self.sansImages[int(self.frame / speed)],
            (Constants["centerx"] - 100, self.sansStartY),
        )

        sayFrameW = 4

        if self.boSay:
            sayFrameW = 10

        if self.saying:
            if self.sayingFrame % sayFrameW == 0 and int(
                self.sayingFrame / sayFrameW
            ) < len(self.gonnaSay):
                if self.gonnaSay[int(self.sayingFrame / sayFrameW)] != "\1":
                    if self.boSay == False:
                        self.sansSpeakSound.play()
                    self.saied = (
                        self.saied + self.gonnaSay[int(self.sayingFrame / sayFrameW)]
                    )
            self.sayingFrame += 1
            drawImage(
                "images/sans/message.png",
                Constants["centerx"] + 105,
                self.sansStartY + 30,
                270,
                100,
            )
            spli = self.saied.split("\n")
            tcolr = Color["BLACK"]

            if self.boSay == True:
                tcolr = Color["RED"]

            for i in range(len(spli)):
                writeText(
                    self.screen,
                    spli[i],
                    Font["text"](FontSize["div"]),
                    tcolr,
                    Constants["centerx"] + 105 + 40 + 5,
                    self.sansStartY + 30 + 10 + 5 + (FontSize["div"] * i),
                    None,
                    Align.LEFT,
                )

            if int(self.sayingFrame / sayFrameW) > len(self.gonnaSay) + 15:
                self.saied = ""
                self.gonnaSay = ""
                self.saying = False
                self.sayingFrame = 0

    def sansSays(self):
        global frame

        if frame == 60:
            self.say("it's a beautiful\n\1day outside.")

        if frame == 310:
            self.say("birds are singing,\n\1\1\1\1flowers are\nblooming...\1\1")

        if frame == 610:
            self.say("on days like these,\n\1kids like you...")
        if frame == 1000:
            self.boldSay("Should be burning\nin hell.")


class ComponentHPBar(Screen):
    hpBarWidth = 250
    hpBarHeight = 32
    hpBarX: int
    hpBarY = yflex(8, 10)

    def __init__(self, screen):
        super().__init__(screen)
        self.hpBarX = Constants["centerx"] - int(self.hpBarWidth / 2) - 32

    def build(self):
        global hp

        hpCanBe = (self.hpBarWidth - kr) / self.hpBarWidth * maxHP

        if hp > hpCanBe:
            hp = hpCanBe

        drawRect(
            Color["RED"],
            self.hpBarX,
            self.hpBarY,
            self.hpBarWidth,
            self.hpBarHeight,
        )

        drawRect(
            Color["GREEN"],
            self.hpBarX,
            self.hpBarY,
            int(self.hpBarWidth * hp / maxHP),
            self.hpBarHeight,
        )
        krSt = int(self.hpBarWidth * hp / maxHP)
        krEd = krSt + kr
        if krEd > self.hpBarWidth:
            krEd = self.hpBarWidth

        if krSt < krEd:
            drawRect(
                Color["PURPLE"],
                self.hpBarX + krSt,
                self.hpBarY,
                krEd - krSt,
                self.hpBarHeight,
            )
        writeText(
            self.screen,
            "HP",
            Font["text"](FontSize["h3"]),
            Color["WHITE"],
            self.hpBarX - FontSize["h3"] * 2,
            self.hpBarY + int(FontSize["h3"] / 2.3),
            None,
            Align.LEFT,
        )


class ComponentKR(Screen):
    frame = 0

    def __init__(self, screen):
        super().__init__(screen)
        self.frame = 0

    def build(self):
        global kr
        self.frame += 1
        if self.frame >= 50:
            kr -= 1
            self.frame = 0
        if kr < 1:
            kr = 1
        col = Color["PURPLE"]
        if kr == maxKR:
            col = Color["WHITE"]
        if kr == 1:
            col = Color["WHITE"]
        writeText(
            self.screen,
            f"KR {kr}/{maxKR}",
            Font["text"](FontSize["h3"]),
            col,
            Constants["centerx"] + 100 + 32,
            yflex(8, 10) + int(FontSize["h3"] / 2.3),
            None,
            Align.LEFT,
        )


class ComponentOptions(Screen):
    plOption1: ComponentButton
    plOption2: ComponentButton
    plOption3: ComponentButton
    plOption4: ComponentButton

    selected: int = 0

    def __init__(self, screen):
        super().__init__(screen)
        self.selected = 0
        self.plOption1 = ComponentButton(self.screen, "ATK", xflex(2, 8))
        self.plOption1.selected = True
        self.plOption2 = ComponentButton(self.screen, "ACT", xflex(3, 8))
        self.plOption3 = ComponentButton(self.screen, "ITM", xflex(4, 8))
        self.plOption4 = ComponentButton(self.screen, "MRC", xflex(5, 8))

    def onKeyUp(self, e: KeyEvent):
        if e.keyCode == KeyCode["ARROW_RIGHT"]:
            self.selected += 1
            self.selected %= 4
        if e.keyCode == KeyCode["ARROW_LEFT"]:
            self.selected -= 1
            if self.selected < 0:
                self.selected = 3

    def build(self):
        self.plOption1.selected = isMyTurn and self.selected == 0
        self.plOption2.selected = isMyTurn and self.selected == 1
        self.plOption3.selected = isMyTurn and self.selected == 2
        self.plOption4.selected = isMyTurn and self.selected == 3

        self.plOption1.build()
        self.plOption2.build()
        self.plOption3.build()
        self.plOption4.build()


class ComponentGameLand(Screen):
    animating = False
    newX = 0
    newY = 0
    oldX = 0
    oldY = 0
    frame = 0

    def newSize(self, newX: int, newY: int):
        self.newX = newX
        self.newY = newY

        self.oldX = gameLandWidth
        self.oldY = gameLandHeight

        self.animating = True
        self.frame = 0

    def build(self):
        global gameLandWidth, gameLandHeight

        if self.animating:
            if self.frame <= sec2frame(0.3):
                gameLandWidth = int(
                    self.oldX + (self.newX - self.oldX) * self.frame / sec2frame(0.3)
                )
                gameLandHeight = int(
                    self.oldY + (self.newY - self.oldY) * self.frame / sec2frame(0.3)
                )
                print(f"{gameLandWidth} {gameLandHeight}")
                self.frame += 1
            else:
                self.animating = False

        xy = gmaeLandXY()
        drawBorder(
            Color["WHITE"],
            xy[0],
            xy[1],
            gameLandWidth,
            gameLandHeight,
            5,
        )


class ComponentPlayer(Screen):
    playerImgs: list[pygame.Surface]
    movingDirs = []

    def __init__(self, screen):
        super().__init__(screen)
        self.playerImgs = []
        self.movingDirs = []

        playerImg = pygame.image.load("images/player.png")
        playerImg = pygame.transform.scale(playerImg, (playerSize, playerSize))
        self.playerImgs.append(playerImg)
        playerImg = pygame.image.load("images/gplayer.png")
        playerImg = pygame.transform.scale(playerImg, (playerSize, playerSize))
        self.playerImgs.append(pygame.transform.rotate(playerImg, 90))
        self.playerImgs.append(pygame.transform.rotate(playerImg, -90))
        self.playerImgs.append(playerImg)
        self.playerImgs.append(pygame.transform.rotate(playerImg, 180))

    def onKeyDown(self, e: KeyEvent):
        if e.keyCode in [
            KeyCode["ARROW_DOWN"],
            KeyCode["ARROW_LEFT"],
            KeyCode["ARROW_RIGHT"],
            KeyCode["ARROW_UP"],
        ]:
            try:
                self.movingDirs.append(e.keyCode)
            except:
                pass

    def onKeyUp(self, e: KeyEvent):
        if e.keyCode in [
            KeyCode["ARROW_DOWN"],
            KeyCode["ARROW_LEFT"],
            KeyCode["ARROW_RIGHT"],
            KeyCode["ARROW_UP"],
        ]:
            self.movingDirs.remove(e.keyCode)

    def build(self):
        global playerX
        global playerY
        self.screen.blit(
            self.playerImgs[gravityDir],
            (
                playerX + int(Constants["centerx"] - gameLandWidth / 2 + 5) + borderDX,
                playerY + yflex(1, 2) + 5 + borderDY,
            ),
        )

        gaviter = True

        if not cannotMove:
            for dir in self.movingDirs:
                if dir == KeyCode["ARROW_DOWN"]:
                    playerY += playerSpeed
                    if gravityDir == 4:
                        gaviter = False
                if dir == KeyCode["ARROW_UP"]:
                    playerY -= playerSpeed
                    if gravityDir == 3:
                        gaviter = False
                if dir == KeyCode["ARROW_RIGHT"]:
                    playerX += playerSpeed
                    if gravityDir == 2:
                        gaviter = False
                if dir == KeyCode["ARROW_LEFT"]:
                    playerX -= playerSpeed
                    if gravityDir == 1:
                        gaviter = False

        if gaviter:
            playerX += gravityDX[gravityDir]
            playerY += gravityDY[gravityDir]

        if playerX < 0:
            playerX = 0
        if playerY < 0:
            playerY = 0
        if playerX > gameLandWidth - int(playerSize * 1.4):
            playerX = gameLandWidth - int(playerSize * 1.3)
        if playerY > gameLandHeight - int(playerSize * 1.3):
            playerY = gameLandHeight - int(playerSize * 1.3)


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


class EntityGasterBlaster(Screen):
    imgs: list[pygame.Surface] = []
    x: int
    y: int
    frame: int = 0
    rot: int

    def __init__(self, screen, x: int, y: int, rotation: int = 0):
        super().__init__(screen)
        self.x = x
        self.y = y
        self.rot = rotation
        for i in range(5):
            self.imgs.append(
                pygame.transform.scale2x(
                    pygame.transform.rotate(
                        pygame.image.load(f"images/GasterBlaster/{i}.png"),
                        rotation - 90,
                    )
                )
            )

    def build(self):
        if self.frame < sec2frame(0.2):
            self.screen.blit(
                self.imgs[int(self.frame / (sec2frame(0.2) / 4))], (self.x, self.y)
            )
        else:
            rect = pygame.Surface(
                (Constants["screenx"] * 2, self.imgs[4].get_rect().height)
            )
            rect = pygame.transform.rotate(rect, self.rot - 90)
            rect.fill(Color["WHITE"])
            self.screen.blit(rect, (self.x, self.y))
            self.screen.blit(self.imgs[4], (self.x, self.y))
        self.frame += 1


class InGameScreen(Screen):
    sans: ComponentSans
    hpBar: ComponentHPBar
    krBar: ComponentKR
    optionsCC: ComponentOptions
    gameLand: ComponentGameLand
    player: ComponentPlayer

    entities: list[tuple[int, EntityGasterBlaster]] = []

    def __init__(self, screen):
        super().__init__(screen)
        global attackSound
        global damagedSound
        global dingSound
        attackSound = pygame.mixer.Sound("audio/atk.ogg")
        damagedSound = pygame.mixer.Sound("audio/dmg.ogg")
        dingSound = pygame.mixer.Sound("audio/ding.ogg")

    def init(self):
        global frame

        self.sans = ComponentSans(self.screen)
        self.hpBar = ComponentHPBar(self.screen)
        self.krBar = ComponentKR(self.screen)
        self.optionsCC = ComponentOptions(self.screen)
        self.gameLand = ComponentGameLand(self.screen)
        self.player = ComponentPlayer(self.screen)

        frame = 0
        self.entities.append((0, EntityGasterBlaster(self.screen, 0, 0, 90)))

    def drawStats(self):
        self.krBar.build()
        self.hpBar.build()

    def mustDraws(self):
        self.screen.fill("black")

        self.sans.sansSays()
        self.sans.build()
        self.drawStats()
        self.optionsCC.build()
        self.player.build()
        self.gameLand.build()

        writeText(
            screen=self.screen,
            text=f"FRAME | {frame} ({frame2sec(frame)}s)",
            font=Font["text"](FontSize["div"]),
            color=Color["WHITE"],
            x=Constants["screenx"] - FontSize["div"],
            y=FontSize["div"],
            bgColor=None,
            align=Align.RIGHT,
        )

    def onKeyUp(self, e: KeyEvent):
        global gravityDir
        self.optionsCC.onKeyUp(e)
        self.player.onKeyUp(e)

        if e.keyCode == KeyCode["ESC"]:
            route.push("/pause")

        if e.keyCode == KeyCode["ENTER"]:
            gravityDir = (gravityDir + 1) % 5

    def onKeyDown(self, e: KeyEvent):
        self.player.onKeyDown(e)

    def shakeScreen(self):
        copied = self.screen.copy()
        self.screen.fill("black")
        self.screen.blit(copied, getShakeOffest())

    def step1(self):
        global cannotMove, gravityDir
        # 위에서 아래로 중력을 강하게 하여 내리는거
        if frame == 1300:
            playAttackSound()
            gravityDir = 3
            setGravity(1000)
            cannotMove = True
        if 1330 >= frame >= 1300:
            self.shakeScreen()
        if frame == 1325:
            setGravity(7)
            cannotMove = False

    def step2(self):
        global gravityDir
        # 뼈 아래서 위로 올라가는거 13.133 ~ 13.767
        if 1370 >= frame >= 1361:
            xy = gmaeLandXY()
            drawBorder(
                Color["RED"],
                xy[0],
                xy[1] + gameLandHeight - (20 * (playerSpeed + 1)),
                gameLandWidth,
                (20 * (playerSpeed + 1)),
                5,
            )
        if 1373 >= frame >= 1372:
            boneHei = flex(gameLandHeight, 1, 5)
            for i in range(0, gameLandWidth - 1, 16):
                EntityBone(self.screen, False, 0).build(
                    i,
                    gameLandHeight - boneHei,
                    10000,
                )
        if 1375 >= frame >= 1374:
            boneHei = flex(gameLandHeight, 1, 3)
            for i in range(0, gameLandWidth - 1, 16):
                EntityBone(self.screen, False, 0).build(
                    i,
                    gameLandHeight - boneHei,
                    10000,
                )
        if 1449 >= frame >= 1376:
            boneHei = flex(gameLandHeight, 4, 10)
            for i in range(0, gameLandWidth - 1, 16):
                EntityBone(self.screen, False, 0).build(
                    i,
                    gameLandHeight - boneHei,
                    10000,
                )
        if frame == 1400:
            dingSound.play()
            gravityDir = 0

    def step3(self):
        # 뼈 Wave 14.183 ~ 15.900
        if v2f(15.900) >= frame >= v2f(14.183):
            for boneUD in range(len(upDownBones)):
                upBoneHeight = int(upDownBones[boneUD][0] * playerSize)
                downBoneHeight = upDownBones[boneUD][1] * playerSize
                speedPF = int(gameLandWidth / 25)
                EntityBone(self.screen, False, 0).build(
                    (frame - 1434) * speedPF - (32 * boneUD),
                    0,
                    upBoneHeight,
                )
                EntityBone(self.screen, False, 0).build(
                    (frame - 1434) * speedPF - (32 * boneUD),
                    gameLandHeight - downBoneHeight,
                    downBoneHeight,
                )

    def build(self):
        global frame, playerDamagedInThisFrame

        if isMyTurn == False:
            frame += 1

        self.mustDraws()

        # 60 FPS -> 30 FPS for Attack
        if frame % 2 == 0:
            playerDamagedInThisFrame = False

        self.step1()
        self.step2()
        self.step3()

        for i in self.entities:
            if i[0] + 180 < frame:
                del i
                continue
            i[1].build()
