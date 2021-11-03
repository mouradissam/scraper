from .abstract_backend import AbstractBackend
from ..link_data import LinkData
from typing import List


class MemoryBackend(AbstractBackend):
    def __init__(self, moniker: str = "MemoryBackend", **kwargs) -> None:
        super().__init__(moniker, **kwargs)
        self.data = []

    async def setup(self):
        pass

    async def tear_down(self):
        pass

    async def pop_batch(self, data: List[LinkData]) -> None:
        for linkdata in data:
            self.data.append(linkdata)
