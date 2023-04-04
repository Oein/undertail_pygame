from enum import Enum
from typing import Callable, TypedDict
import pygame


class DictTypeColor(TypedDict):
    WHITE: pygame.Color
    RED: pygame.Color
    GREEN: pygame.Color
    BLUE: pygame.Color
    PURPLE: pygame.Color
    YELLOW: pygame.Color
    ORANGE: pygame.Color
    BLACK: pygame.Color


class DictTypeFont(TypedDict):
    title: Callable[[int], pygame.font.Font]
    text: Callable[[int], pygame.font.Font]


class DictTypeConstants(TypedDict):
    screenx: int
    screeny: int
    centerx: int
    centery: int
    framerate: int


class DictTypeFontSize(TypedDict):
    h1: int
    h2: int
    h3: int
    div: int


class DictTypeKeyCode(TypedDict):
    ARROW_UP: int
    ARROW_DOWN: int
    ARROW_LEFT: int
    ARROW_RIGHT: int
    ENTER: int
    ESC: int


class Align(Enum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2
