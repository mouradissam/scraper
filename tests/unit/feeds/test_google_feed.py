import asynctest
from scraper.feeds.google_feed import GoogleFeed
from ..listeners.mock_listener import MockListener


class TestGoogleFeed(asynctest.TestCase):
    def test_constructor(self):
        feed = GoogleFeed(MockListener())
        self.assertEqual(feed.moniker, "GoogleFeed")
        self.assertEqual(feed.listener.moniker, "MockListener")
        self.assertEqual(feed.default_location, "Austin,Texas")

    async def search_coroutine(self):
        feed = GoogleFeed(MockListener())
        await feed.search_cmd(["Bitcoin"])
        self.assertNotEqual(len(feed.listener.data), 0)

    def test_search(self):
        self.loop.run_until_complete(self.search_coroutine())


if __name__ == "__main__":
    asynctest.main()
