from oein import *
import pygame
from screens.InGame import getFrame
from constants.SansMessages import messages


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
        msg = messages.get(getFrame())
        if msg is not None:
            if msg[1]:
                self.boldSay(msg[0])
            else:
                self.say(msg[0])
