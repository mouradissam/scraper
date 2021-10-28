import asynctest
from asynctest.mock import Mock
from scraper.listeners.reactor_listener import ReactorListener
from scraper.link_data import LinkData
from ..workers.mock_worker import MockWorker


class TestReactorListener(asynctest.TestCase):
    def test_constructor(self):
        listener = ReactorListener(worker=MockWorker(loop=self.loop))
        self.assertEqual(listener.moniker, "ReactorListener")
        self.assertEqual(listener.worker.moniker, "MockWorker")

    async def push_coroutine(self):
        worker = MockWorker(loop=self.loop)    
        listener = ReactorListener(worker=worker)

        await listener.start()

        await listener.push([LinkData("Link1"), LinkData("Link2")])
        await listener.stop()
        await listener.worker.stop()
        self.assertEqual(len(worker.data), 2)

    def test_push(self):
        self.loop.run_until_complete(self.push_coroutine())


if __name__ == "__main__":
    asynctest.main()
