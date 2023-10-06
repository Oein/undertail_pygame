import pygame
import route
import random
import math
from dictClassType import *

from constants.PygameAttributes import *


class KeyEvent:
    def __init__(
        self, text: str, keyCode: int, mod: int, scancode: int, type: int
    ) -> None:
        self.text = text
        self.keyCode = keyCode
        self.mod = mod
        self.scancode = scancode
        self.type = type

    text: str
    keyCode: int
    mod: int
    scancode: int
    type: int


class Screen:
    screen: pygame.Surface

    def __init__(self, screen):
        self.screen = screen

    def onKeyDown(self, e: KeyEvent):
        print(f"[Key][Press] {e.keyCode}, {e.mod}")
        pass

    def onKeyUp(self, e: KeyEvent):
        print(f"[Key][Release] {e.keyCode}, {e.mod}")
        pass

    def onPause(self):
        pass

    def onLoad(self):
        pass

    def build(self):
        self.superBuild()

    def superBuild(self):
        writeText(
            screen=self.screen,
            text=f"PATH | {route.path}",
            font=Font["text"](FontSize["div"]),
            color=Color["WHITE"],
            x=FontSize["div"],
            y=FontSize["div"],
            bgColor=None,
            align=Align.LEFT,
        )


Font = DictTypeFont(
    title=lambda size: pygame.font.Font("fonts/title.ttf", size),
    text=lambda size: pygame.font.Font("fonts/chat.ttf", size),
)

Color = DictTypeColor(
    WHITE=pygame.Color(255, 255, 255),
    RED=pygame.Color(255, 0, 0),
    GREEN=pygame.Color(0, 255, 0),
    BLUE=pygame.Color(0, 0, 255),
    PURPLE=pygame.Color(255, 0, 255),
    YELLOW=pygame.Color(255, 255, 0),
    ORANGE=pygame.Color(255, 165, 0),
    BLACK=pygame.Color(0, 0, 0),
)

FontSize = DictTypeFontSize(h1=64, h2=50, h3=36, div=24)

KeyCode = DictTypeKeyCode(
    ARROW_UP=1073741906,
    ARROW_DOWN=1073741905,
    ARROW_LEFT=1073741904,
    ARROW_RIGHT=1073741903,
    ENTER=13,
    ESC=27,
)

from screen import screen


def flex(full: int, flex_: int, maxflex: int):
    if maxflex < flex_:
        flex_ = maxflex

    return int(full * flex_ / maxflex)


def xflex(flex_: int, maxflex: int):
    return flex(Constants["screenx"], flex_, maxflex)


def yflex(flex_: int, maxflex: int):
    return flex(Constants["screeny"], flex_, maxflex)


def writeText(
    screen: pygame.Surface,
    text: str,
    font: pygame.font.Font,
    color: pygame.Color,
    x: int,
    y: int,
    bgColor: pygame.Color | None,
    align: Align,
):
    myText = font.render(text, True, color, bgColor)
    myTextArea = myText.get_rect()
    if align == Align.CENTER:
        myTextArea.center = (x, y)
    if align == Align.LEFT:
        myTextArea.center = (x + int(myTextArea.width / 2), y)
    if align == Align.RIGHT:
        myTextArea.center = (x - int(myTextArea.width / 2), y)

    screen.blit(myText, myTextArea)

    return (myText, myTextArea)


def drawBorder(
    color: pygame.Color, x: int, y: int, width: int, height: int, borderSize: int = 2
):
    pygame.draw.rect(screen, color, pygame.Rect(x, y, width, height), borderSize)


def drawRect(
    background: pygame.Color,
    x: int,
    y: int,
    width: int,
    height: int,
    borderSize: int = 2,
    borderColor: pygame.Color | None = None,
):
    pygame.draw.rect(screen, background, pygame.Rect(x, y, width, height))
    if borderColor != None:
        pygame.draw.rect(
            screen, borderColor, pygame.Rect(x, y, width, height), borderSize
        )


def sec2frame(sec: float):
    return int(sec * Constants["framerate"])


def frame2sec(frame: int):
    return math.floor(frame / Constants["framerate"] * 10) / 10


def drawImage(
    src: str,
    x: int,
    y: int,
    width: int,
    height: int,
):
    img = pygame.image.load(src)
    img = pygame.transform.scale(img, (width, height))
    screen.blit(img, (x, y))


def getShakeOffest():
    return (random.randint(-4, 4), random.randint(-4, 4))


def videoSecToFrame(videoSec: float):
    return (videoSec - 12) * 60 + 1300


v2f = videoSecToFrame
