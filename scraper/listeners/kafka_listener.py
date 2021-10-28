from abc import ABC, abstractmethod
import logging
from .abstract_listener import AbstractListener
from ..link_data import LinkData
from ..workers.abstract_worker import AbstractWorker
import asyncio
from contextlib import asynccontextmanager
from typing import List

class KafkaListener(AbstractListener):
    default_params = {"topic_name": "link_store"} 

    def __init__(
        self, worker: AbstractWorker, moniker: str = "ReactorListener", **kwargs
    ) -> None:
        self.__dict__.update(self.default_params)
        super().__init__(moniker=moniker, worker=worker, **kwargs)

    async def setup(self):
        raise NotImplementedError("")

    async def tear_down(self):
        raise NotImplementedError("")

    async def push(self, data: List[LinkData]) -> None:
        raise NotImplementedError()
