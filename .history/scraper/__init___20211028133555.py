import argparse
import logging
import logging.config
import yaml

import asyncio
from scraper.feeds.google_feed import GoogleFeed
from scraper.listeners.reactor_listener import ReactorListener
from scraper.backends.memory_backend import MemoryBackend
from scraper.workers.reactor_worker import ReactorWorker


def setup_loging() -> None:
    with open("scraper/config/logging.yaml", "r") as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)
        logging.config.dictConfig(config)


LOG = logging.getLogger("vaper")


async def main(loop: asyncio.AbstractEventLoop) -> None:
    parser = argparse.ArgumentParser(
        description="Versatil data scraper",
        argument_default=argparse.SUPPRESS,
    )
    parser.add_argument(
        "-q",
        "--query",
        dest="query",
        default="how to data engineering",
        help="search query",
    )
    args = vars(parser.parse_args())

    try:
        backend = MemoryBackend(loop=loop)
        worker = ReactorWorker(backend=backend)
        listener = ReactorListener(worker=worker)
        google_feed = GoogleFeed(listener=listener)

        async with google_feed.boot() as feed:
            await feed.search_cmd([args['query']])
    except Exception as e:
        LOG.error("Exception: {0}".format(e))
    finally:
        LOG.info("exiting, bye bye...")


if __name__ == "__main__":
    setup_loging()
    LOG.info("Starting...")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
