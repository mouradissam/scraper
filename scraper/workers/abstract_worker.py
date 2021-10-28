from abc import ABC, abstractmethod
import logging
from enum import Enum
import time
from typing import List
from ..backends.abstract_backend import AbstractBackend
from ..link_data import LinkData

LOG = logging.getLogger("vaper")


class Status(Enum):
    RUNNING = 0
    STOPPED = 1
    SUSPENDED = 2


class AbstractWorker(ABC):
    default_params = {"status": Status.STOPPED}

    def __init__(self, moniker: str, backend: AbstractBackend, **kwargs) -> None:
        self.__dict__.update(kwargs)
        self.moniker = moniker
        self.backend = backend
        self.status = Status.STOPPED

    async def start(self) -> None:
        if self.status != Status.RUNNING:
            LOG.info(f"starting worker {self.moniker}...")
            self.status = Status.RUNNING
            self.start_time = time.time()
            if self.backend.status != Status.RUNNING:
                await self.backend.start()
            await self.setup()
            self.end_time = time.time()

    async def stop(self) -> None:
        if self.status != Status.STOPPED:
            LOG.info(
                f"stopping worker {self.moniker}... Uptime {self.end_time - self.start_time:.2f}s"
            )
            await self.tear_down()
            self.status = Status.STOPPED

    @abstractmethod
    async def setup(self):
        raise NotImplementedError()

    @abstractmethod
    async def tear_down(self):
        raise NotImplementedError()

    @abstractmethod
    async def push(self, data: LinkData) -> None:
        raise NotImplementedError()
