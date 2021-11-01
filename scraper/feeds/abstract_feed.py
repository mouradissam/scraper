import logging
from abc import ABC, abstractmethod
import time
from enum import Enum
from contextlib import asynccontextmanager
from ..listeners.abstract_listener import AbstractListener

LOG = logging.getLogger("vaper")


class Status(Enum):
    RUNNING = 0
    STOPPED = 1
    SUSPENDED = 2


class AbstractFeed(ABC):
    default_params = {"status": Status.STOPPED}

    def __init__(self, listener: AbstractListener, **kwargs) -> None:
        self.__dict__.update(self.default_params)
        self.__dict__.update(kwargs)
        self.status = Status.STOPPED
        self.listener = listener

    async def start(self) -> None:
        if self.status != Status.RUNNING:
            self.status = Status.RUNNING
            self.start_time = time.time()
            if self.listener.status != Status.RUNNING:
                await self.listener.start()
            await self.setup()
            self.end_time = time.time()

    async def stop(self) -> None:
        if self.status != Status.STOPPED:
            LOG.info(
                f"stopping feed {self.moniker}... "
                f"Uptime {self.end_time - self.start_time:.2f}s"
            )
            await self.tear_down()
            self.status = Status.STOPPED

    @abstractmethod
    async def setup(self, **kwargs) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def tear_down(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def search_cmd(self, queries, location=None, **kwargs) -> None:
        raise NotImplementedError()

    @asynccontextmanager
    async def boot(self):
        await self.start()
        yield self
        await self.stop()
        await self.listener.stop()
        await self.listener.worker.stop()
        await self.listener.worker.backend.stop()
