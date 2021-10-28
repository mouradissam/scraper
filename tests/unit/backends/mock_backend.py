from typing import List
from scraper.link_data import LinkData
from scraper.backends.abstract_backend import AbstractBackend


class MockBackend(AbstractBackend):
    def __init__(self, moniker: str = "MockBackend", **kwargs) -> None:
        super().__init__(moniker, **kwargs)
        self.data = []

    async def setup(self):
        pass

    async def tear_down(self):
        pass

    async def pop_batch(self, data: List[LinkData]) -> None:
        for linkdata in data:
            self.data.append(linkdata)
