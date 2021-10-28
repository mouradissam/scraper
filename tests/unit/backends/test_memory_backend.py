import asynctest

from scraper.backends.memory_backend import MemoryBackend
from scraper.link_data import LinkData 


class TestReactorListener(asynctest.TestCase):
    # def setUp(self):
    #     self.loop = asyncio.new_event_loop()

    def test_constructor(self):
        backend = MemoryBackend(loop=self.loop)
        self.assertEqual(backend.moniker, "MemoryBackend")

    async def push_coroutine(self):
        MIN_BATCH_SIZE = 3
        backend = MemoryBackend(loop=self.loop, min_batch_size=MIN_BATCH_SIZE)
        await backend.start()

        await backend.push(
            [LinkData("Link1"), LinkData("Link2"), LinkData("link3"), LinkData("link4")]
        )
        await backend.stop()
        self.assertEqual(len(backend.data), MIN_BATCH_SIZE + 1)

    def test_push(self):
        self.loop.run_until_complete(self.push_coroutine())


if __name__ == "__main__":
    asynctest.main()
