from abc import ABC, abstractmethod
import logging
from enum import Enum
import time
from typing import List
import asyncio
from asyncio.queues import Queue
from contextlib import asynccontextmanager
from ..link_data import LinkData

LOG = logging.getLogger("vaper")


class Status(Enum):
    RUNNING = 0
    STOPPED = 1
    SUSPENDED = 2


class AbstractBackend(ABC):
    default_params = {
        "status": Status.STOPPED,
        "max_batch_size": 100,
        "min_batch_size": 1,
    }

    def __init__(self, moniker: str, loop: asyncio.AbstractEventLoop, **kwargs) -> None:
        self.__dict__.update(self.default_params)
        self.__dict__.update(kwargs)
        self.moniker = moniker
        self.loop = loop
        self.queue = Queue()
        self.status = Status.STOPPED

    @asynccontextmanager
    async def read_queue(self):
        update = await self.queue.get()
        yield update
        self.queue.task_done()

    @asynccontextmanager
    async def read_many_queue(self, count: int):
        # TODO: add a timer
        ret = [await self.queue.get() for _ in range(count)]
        yield ret
        for _ in range(count):
            self.queue.task_done()

    async def start(self) -> None:
        if self.status != Status.RUNNING:
            LOG.info(f"starting backend {self.moniker}...")
            self.status = Status.RUNNING
            self.start_time = time.time()
            self.pop_task = self.loop.create_task(self.pop())
            await self.setup()
            self.end_time = time.time()

    async def stop(self) -> None:
        if self.status != Status.STOPPED:
            self.status = Status.STOPPED
            LOG.info(
                f"stopping listener {self.moniker}... "
                f"Uptime {self.end_time - self.start_time:.2f}s"
            )
            await self.queue.join()
            self.pop_task.cancel()
            await asyncio.gather(self.pop_task, return_exceptions=True)
            await self.tear_down()

    async def push(self, data: List[LinkData]) -> None:
        for backdata in data:
            await self.queue.put(backdata)

    async def pop(self):
        while True:
            size = min(
                self.max_batch_size, max(self.queue.qsize(), self.min_batch_size)
            )
            async with self.read_many_queue(size) as data:
                await self.pop_batch(data)

    @abstractmethod
    async def setup(self):
        raise NotImplementedError()

    @abstractmethod
    async def tear_down(self):
        raise NotImplementedError()

    @abstractmethod
    async def pop_batch(self, updates: list):
        raise NotImplementedError()
