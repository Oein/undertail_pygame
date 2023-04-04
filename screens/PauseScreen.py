from oein import *
import route


class PauseScreen(Screen):
    options = ["Resume", "To main screen", "Exit"]

    def __init__(self, screen):
        Screen.__init__(self, screen)
        self.option = 0

    def onKeyUp(self, e: KeyEvent):
        if e.keyCode == KeyCode["ARROW_UP"]:
            self.option = self.option - 1
            if self.option < 0:
                self.option = len(self.options) - 1
            return

        if e.keyCode == KeyCode["ARROW_DOWN"]:
            self.option = (self.option + 1) % len(self.options)
            return

        if e.keyCode == KeyCode["ENTER"]:
            if self.option == 2:
                pygame.mixer.music.unpause()
                route.push("/sureToExit")
            if self.option == 0:
                route.back()
            if self.option == 1:
                route.push("/sureToMain")
        if e.keyCode == KeyCode["ESC"]:
            pygame.mixer.music.unpause()
            route.back()

    def build(self):
        pygame.mixer.music.pause()
        self.screen.fill("black")
        writeText(
            screen=self.screen,
            text="- PAUSED -",
            font=Font["title"](FontSize["h1"]),
            color=Color["WHITE"],
            x=Constants["centerx"],
            y=yflex(2, 7),
            bgColor=None,
            align=Align.CENTER,
        )

        for i in range(len(self.options)):
            opt = self.options[i]
            if self.option == i:
                opt = "> " + opt
            writeText(
                screen=self.screen,
                text=opt,
                font=Font["text"](FontSize["h3"]),
                color=Color["WHITE"],
                x=Constants["centerx"],
                y=int(Constants["centery"] * 1.5) + (FontSize["h3"] + 5) * i,
                bgColor=None,
                align=Align.CENTER,
            )
