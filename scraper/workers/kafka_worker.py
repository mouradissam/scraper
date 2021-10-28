from abc import ABC, abstractmethod
import logging
from .abstract_worker import AbstractWorker
from ..link_data import LinkData
from ..backends.abstract_backend import AbstractBackend
import asyncio
from contextlib import asynccontextmanager
from typing import List

LOG = logging.getLogger("KafkaWorker")


class KafkaWorker(AbstractWorker):
    default_params = {"topic_name": "link_snapper"}

    def __init__(
        self, backend: AbstractBackend, moniker: str = "ReactorWorker", **kwargs
    ) -> None:
        self.__dict__.update(self.default_params)
        super().__init__(moniker=moniker, backend=backend, **kwargs)

    async def setup(self):
        raise NotImplementedError()

    async def tear_down(self):
        raise NotImplementedError()

    async def push(self, data: List[LinkData]) -> None:
        raise NotImplementedError()
