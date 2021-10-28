import asynctest
from asynctest.mock import Mock

from scraper.workers.reactor_worker import ReactorWorker
from scraper.link_data import LinkData
from scraper.backends.memory_backend import MemoryBackend
from ..backends.mock_backend import MockBackend


class TestReactorWorker(asynctest.TestCase):
    def test_constructor(self):
        worker = ReactorWorker(MockBackend(loop=self.loop))
        self.assertEqual(worker.moniker, "ReactorWorker")
        self.assertEqual(worker.backend.moniker, "MockBackend")

    async def push_coroutine(self):
        backend = MockBackend(loop=self.loop, min_batch_size=2)
        worker = ReactorWorker(backend=backend, num_workers=1)

        await backend.start()
        await worker.start()

        await worker.push(
            [LinkData("http://www.google.com"), LinkData("http://www.google.it")]
        )
        await worker.stop()
        await backend.stop()
        self.assertEqual(len(backend.data), 2)

    def test_push(self):
        self.loop.run_until_complete(self.push_coroutine())


if __name__ == "__main__":
    asynctest.main()
