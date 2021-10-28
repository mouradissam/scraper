import logging
from serpapi import GoogleSearch
from .abstract_feed import AbstractFeed
from ..listeners.abstract_listener import AbstractListener
from ..link_data import LinkData
from ..exceptions import SearchError


LOG = logging.getLogger("vaper")


class GoogleFeed(AbstractFeed):
    default_params = {"default_location": "Austin,Texas"}

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
        self.location = location if location else self.default_location
        search = GoogleSearch(
            {"location": self.location, "async": True, "api_key": self.api_key}
        )
        for query in queries:
            LOG.info(f"Executing query '{query}'")
            search.params_dict["q"] = query
            result = search.get_dict()
            # if "error" in result:
            #     LOG.error(result["error"])
            #     continue
            for r in result["organic_results"]:
                await self.listener.push([LinkData(r["link"])])
