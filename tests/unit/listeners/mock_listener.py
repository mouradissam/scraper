from typing import List
from scraper.link_data import LinkData
from scraper.listeners.abstract_listener import AbstractListener


class MockListener(AbstractListener):
    def __init__(self, moniker: str = "MockListener", **kwargs) -> None:
        super().__init__(moniker, worker=None, **kwargs)
        self.data = []

    async def setup(self):
        pass

    async def tear_down(self):
        pass

    async def push(self, data: List[LinkData]) -> None:
        self.data.extend(data)
