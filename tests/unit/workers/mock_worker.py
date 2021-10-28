from typing import List
from scraper.workers.abstract_worker import AbstractWorker
from scraper.link_data import LinkData
from ..backends.mock_backend import MockBackend


class MockWorker(AbstractWorker):
    def __init__(self, moniker: str = "MockWorker", loop=None, **kwargs) -> None:
        super().__init__(moniker=moniker, backend=MockBackend(loop=loop), **kwargs)
        self.data = []

    async def setup(self):
        pass

    async def tear_down(self):
        pass

    async def push(self, data: List[LinkData]) -> None:
        for linkdata in data:
            self.data.append(linkdata)
