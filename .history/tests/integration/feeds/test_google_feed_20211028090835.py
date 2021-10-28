import asynctest
from asynctest.mock import Mock
from scraper.feeds.google_feed import GoogleFeed
from scraper.listeners.reactor_listener import ReactorListener
from scraper.backends.memory_backend import MemoryBackend
from scraper.workers.reactor_worker import ReactorWorker


class TestGoogleFeedWorkflow(asynctest.TestCase):
    def test_constructor(self):
        backend = MemoryBackend(loop=self.loop)
        worker = ReactorWorker(backend=backend)
        listener = ReactorListener(worker=worker)
        feed = GoogleFeed(listener=listener)

        self.assertEqual(backend.moniker, "MemoryBackend")
        self.assertEqual(worker.moniker, "ReactorWorker")
        self.assertEqual(listener.moniker, "ReactorListener")
        self.assertEqual(feed.moniker, "GoogleFeed")

    async def search_coroutine(self):
        backend = MemoryBackend(loop=self.loop)
        worker = ReactorWorker(backend=backend)
        listener = ReactorListener(worker=worker)
        feed = GoogleFeed(listener=listener)

        await feed.start()
        await feed.search_cmd(["Bitcoin"])
        await listener.stop()
        await worker.stop()
        await backend.stop()
        self.assertEqual(len(backend.data), 8)

    async def search_coroutine_ctx(self):
        backend = MemoryBackend(loop=self.loop)
        worker = ReactorWorker(backend=backend)
        listener = ReactorListener(worker=worker)
        google_feed = GoogleFeed(listener=listener)

        async with google_feed.boot() as feed:
            await feed.search_cmd(["Bitcoin"])

        self.assertEqual(len(backend.data), 8)

    def test_search(self):
        self.loop.run_until_complete(self.search_coroutine())

    def test_search_ctx(self):
        self.loop.run_until_complete(self.search_coroutine_ctx())


if __name__ == "__main__":
    asynctest.main()
