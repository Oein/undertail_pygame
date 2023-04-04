from oein import *
import common


class SureToExit(Screen):
    def __init__(self, screen):
        super().__init__(screen)
        self.option = 0

    def onKeyUp(self, e: KeyEvent):
        if e.keyCode == KeyCode["ARROW_LEFT"]:
            self.option = self.option - 1
            if self.option < 0:
                self.option = 1
            return

        if e.keyCode == KeyCode["ARROW_RIGHT"]:
            self.option = (self.option + 1) % 2
            return

        if e.keyCode == KeyCode["ENTER"]:
            if self.option == 1:
                common.running = False
            else:
                route.back()

    def build(self):
        self.screen.fill("black")
        writeText(
            screen=self.screen,
            text="Are you sure to exit?",
            font=Font["title"](FontSize["h2"]),
            color=Color["WHITE"],
            x=Constants["centerx"],
            y=yflex(1, 3),
            bgColor=None,
            align=Align.CENTER,
        )
        text = ""
        if self.option == 0:
            text = "> No"
        else:
            text = "No"
        text += "                "
        if self.option == 1:
            text += "> Yes"
        else:
            text += "Yes"
        writeText(
            screen=self.screen,
            text=text,
            font=Font["text"](FontSize["h3"]),
            color=Color["WHITE"],
            x=Constants["centerx"],
            y=yflex(2, 3),
            bgColor=None,
            align=Align.CENTER,
        )
