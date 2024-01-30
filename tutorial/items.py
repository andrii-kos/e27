from scrapy import Field, Item

from typing import List

from scrapy.loader import ItemLoader
from itemloaders.processors import Join, MapCompose, TakeFirst


class StartupUrlItem(Item):
    link = Field()


class Startup(Item):
    id: str | None = Field()
    company_name = Field()
    profile_url = Field()
    company_website = Field()
    email = Field(
         output_processor=Join(', ')
    )
    phone = Field(
         output_processor=Join(', ')
    )
    market = Field(
        output_processor=Join(', ')
    )
    founding_date = Field(
        input_processor=MapCompose(str.strip, lambda value: value if value else None),
        output_processor=Join('-')
    )
    founders = Field(
         output_processor=Join(', ')
    )
    location = Field()
    employee_range = Field(
         output_processor=Join(', ')
    )
    urls_social = Field(
        input_processor=MapCompose(str.strip, lambda value: value if value else None),
        output_processor=Join(', ')
    )
    description_short = Field()
    description = Field()


class StartupLoader(ItemLoader):
    default_output_processor = TakeFirst()
