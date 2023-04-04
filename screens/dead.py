from oein import *


class DeadScreen(Screen):
    def build(self):
        self.screen.fill("black")
        writeText(
            self.screen,
            "YOU DEAD",
            Font["title"](FontSize["h1"]),
            Color["RED"],
            Constants["centerx"],
            yflex(1, 3),
            None,
            Align.CENTER,
        )
