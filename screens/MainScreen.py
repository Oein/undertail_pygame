from oein import *
import common
import route


class MainScreen(Screen):
    options = ["Start", "Exit"]

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
            if self.option == 1:
                route.push("/sureToExit")
            else:
                route.routes["/inGame"].init()  # type: ignore
                route.to("/inGame")
                common.playing = True

    def build(self):
        # route.routes["/inGame"].init()  # type: ignore
        # route.push("/inGame")
        # common.playing = True
        # return

        self.screen.fill("black")
        writeText(
            screen=self.screen,
            text="UNDERTAIL",
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
