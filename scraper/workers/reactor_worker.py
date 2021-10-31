from abc import ABC, abstractmethod
import logging
from .abstract_worker import AbstractWorker
from ..link_data import LinkData
from ..backends.abstract_backend import AbstractBackend
import asyncio
from contextlib import asynccontextmanager
from typing import List
import aiohttp

LOG = logging.getLogger("vaper")


class ReactorWorker(AbstractWorker):
    default_params = {"num_workers": 4, "queue_size": 100, "request_timeout_sec": 5}

    def __init__(
        self, backend: AbstractBackend, moniker: str = "ReactorWorker", **kwargs
    ) -> None:
        self.__dict__.update(self.default_params)
        super().__init__(moniker=moniker, backend=backend, **kwargs)
        self.queue = asyncio.Queue(maxsize=self.queue_size)
        self.loop = backend.loop
        self.workers = []
        self.worker_monikers = []

    @asynccontextmanager
    async def read_queue(self):
        update = await self.queue.get()
        yield update
        self.queue.task_done()

    async def worker(self, moniker):
        LOG.info(f"launching {moniker} ...")
        while True:
            async with self.read_queue() as link:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        link.data, timeout=self.request_timeout_sec, ssl=False
                    ) as response:
                        LOG.debug(f"[{moniker} is downloading link]: {link.data}")
                        resp = await response.text()
                        await self.backend.push([resp])

    async def setup(self):
        for i in range(self.num_workers):
            moniker = f"worker-{i}"
            task = self.loop.create_task(self.worker(moniker))
            self.workers.append(task)
            self.worker_monikers.append(moniker)
        await asyncio.sleep(0.0001)

    async def tear_down(self):
        await self.queue.join()
        for i in range(0, len(self.workers)):
            LOG.debug(f"cancelling {self.worker_monikers[i]}...")
            self.workers[i].cancel()
        await asyncio.gather(*self.workers, return_exceptions=True)

    async def push(self, data: List[LinkData]) -> None:
        for linkdata in data:
            await self.queue.put(linkdata)
