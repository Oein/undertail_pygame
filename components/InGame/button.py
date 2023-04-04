from oein import *


class ComponentButton(Screen):
    name: str
    selected: bool
    x: int

    def __init__(self, screen: pygame.Surface, optName: str, x: int):
        self.screen = screen
        self.selected = False
        self.name = optName
        self.x = x

    def build(self):
        color = Color["ORANGE"]

        if self.selected:
            color = Color["YELLOW"]

        tx = writeText(
            screen=self.screen,
            text=self.name,
            font=Font["text"](FontSize["h2"]),
            color=color,
            x=self.x + int(FontSize["h2"] * 1.2),
            y=yflex(9, 10),
            bgColor=None,
            align=Align.LEFT,
        )

        drawBorder(
            color,
            self.x - 50 + int(FontSize["h2"] * 1.2),
            yflex(9, 10) - int(tx[1].height / 2),
            tx[1].width + 50 + 20,
            tx[1].height + 5,
            3,
        )

        fna = self.name

        if self.selected:
            fna = "SEL"

        drawImage(
            f"images/options/{fna}.png",
            self.x - 50 + int(FontSize["h2"] * 1.2) + 10,
            yflex(9, 10) - 20,
            int(FontSize["h2"] * 0.7),
            int(FontSize["h2"] * 0.9),
        )
