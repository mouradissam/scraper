import logging
from serpapi import GoogleSearch
from .abstract_feed import AbstractFeed
from ..listeners.abstract_listener import AbstractListener
from ..link_data import LinkData
from ..exceptions import SearchError
from queue import Queue
import time
import re
import asyncio


LOG = logging.getLogger("vaper")


class GoogleFeed(AbstractFeed):
    default_params = {
        "default_location": "Austin,Texas",
        "default_res_per_page": 5,
        "default_pause_time": 0.1,
    }

    def __init__(self, listener: AbstractListener = None, **kwargs) -> None:
        super().__init__(moniker="GoogleFeed", listener=listener, **kwargs)
        self.__dict__.update(self.default_params)
        self.api_key = (
            "30ea9916d89c706de49728f863282a9112833556de01693f0a59997e1144faed"
        )

    async def setup(self, **kwargs) -> None:
        pass

    async def tear_down(self) -> None:
        pass

    async def search_cmd(self, queries, location=None, **kwargs) -> None:
        search_queue = Queue()
        self.location = location if location else self.default_location
        search = GoogleSearch(
            {
                "location": self.location,
                "async": True,
                "api_key": self.api_key,
                "num": self.default_res_per_page,
            }
        )
        for query in queries:
            LOG.info(f"Executing query '{query}'")
            search.params_dict["q"] = query
            result = search.get_dict()
            if "error" in result:
                LOG.error(result["error"])
                continue
            search_queue.put(result)

        # wait until all search statuses are cached or success
        while not search_queue.empty():
            result = search_queue.get()
            search_id = result["search_metadata"]["id"]
            search_archived = search.get_search_archive(search_id)
            if re.search(
                "Cached|Success", search_archived["search_metadata"]["status"]
            ):
                for r in result["organic_results"]:
                    await self.listener.push([LinkData(r["link"])])
            else:
                search_queue.put(result)
                await asyncio.sleep(self.default_pause_time)
