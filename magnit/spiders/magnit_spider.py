import datetime
import scrapy
import pytz
from magnit.items import MagnitItem


class QuotesSpider(scrapy.Spider):
    name = "magnit"
    start_urls = [
        "https://magnitcosmetic.ru/catalog/kosmetika/brite_i_epilyatsiya/?perpage=96",
        "https://magnitcosmetic.ru/catalog/kosmetika/detskaya_kosmetika_i_ukhod/?perpage=96",
    ]

    def parse(self, response):
        for href in response.css("a.product__link::attr(href)"):
            yield response.follow(href, callback=self.parse_item)

    def parse_item(self, response):
        url = response.request.url
        timestamp = datetime.datetime.now(tz=pytz.utc)
        RPC = url.split("/")[-2]
        title = " ".join(response.css("h1.action-card__name::text").re(r"\w+"))
        brand = response.css("td.action-card__cell::text")[1].get()
        section = url.split("/")[4:-2]
        # price_data: Dict[str, Union[float, str]]
        # stock: Dict[str, Union[bool, int]]
        assets = {"main_page": response.css("img.product__image").xpath("@src").get()}
        # metadata
        data = response.css("td.action-card__cell::text").getall()
        keys = data[0::2]
        values = data[1::2]
        metadata = dict(zip(keys, values))
        metadata["__description"] = response.css("div.action-card__text").xpath("@text")
        item = MagnitItem(
            timestamp=timestamp,
            url=url,
            RPC=RPC,
            title=title,
            brand=brand,
            section=section,
            assets=assets,
            metadata=metadata,
        )
        return item


# process = CrawlerProcess(settings={
#     "FEEDS": {
#         "items.json": {"format": "json"},
#     },
# })
#
# process.crawl(QuotesSpider)
# process.start()
