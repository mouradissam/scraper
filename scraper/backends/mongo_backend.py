from .abstract_backend import AbstractBackend
from ..link_data import LinkData 
from typing import List

class MongoBackend(AbstractBackend):
    def __init__(self, moniker: str = "MemoryBackend", **kwargs) -> None:
        self.__dict__.update(self.default_params)
        super().__init__(moniker, **kwargs)

    async def setup(self):
        raise NotImplementedError()

    async def tear_down(self):
        raise NotImplementedError()

    async def pop_batch(self, data: List[LinkData]) -> None:
        raise NotImplementedError()
