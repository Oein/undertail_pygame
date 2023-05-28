from typing import TypedDict
from oein import v2f


class DictTypeTimings(TypedDict):
    bgmPlay: int


timings = DictTypeTimings(bgmPlay=v2f(21.650))
