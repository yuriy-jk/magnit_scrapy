# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import datetime
from typing import List, Dict, Union, Optional
from dataclasses import dataclass, field


@dataclass
class MagnitItem:
    timestamp: datetime.datetime
    RPC: str
    url: str
    title: str
    brand: str
    section: List[str]
    # price_data: Dict[str, Union[float, str]]
    # stock: Dict[str, Union[bool, int]]
    assets: Dict[str, Union[str, List[str]]]
    metadata: Dict[str, str]
    variants: int = field(default=1)
    marketings_tags: Optional[List[str]] = field(default=None)
