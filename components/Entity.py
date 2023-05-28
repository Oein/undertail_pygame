from oein import *


class Entity:
    frame: int
    entity: Screen
    entityMaxTime: int

    def __init__(self, entity: Screen, entityTime: int = 360):
        self.entity = entity
        self.frame = 0
        self.entityMaxTime = entityTime

    def build(self):
        self.frame += 1
        if self.frame > self.entityMaxTime:
            return False
        self.entity.build()
        return True
