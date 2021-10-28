from abc import ABC, abstractmethod
import logging
from .abstract_listener import AbstractListener
from ..link_data import LinkData
from ..workers.abstract_worker import AbstractWorker
import asyncio
from contextlib import asynccontextmanager
from typing import List

class ReactorListener(AbstractListener):
    default_params = {"num_workers": 4, "queue_size": 100}

    def __init__(
        self, worker: AbstractWorker, moniker: str = "ReactorListener", **kwargs
    ) -> None:
        super().__init__(moniker=moniker, worker=worker, **kwargs)
        self.__dict__.update(self.default_params)

    async def setup(self):
        pass

    async def tear_down(self):
        pass

    async def push(self, data: List[LinkData]) -> None:
        await self.worker.push(data)
