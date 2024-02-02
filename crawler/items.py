from scrapy import Field, Item

from typing import List

from scrapy.loader import ItemLoader
from itemloaders.processors import Join, MapCompose, TakeFirst
import re

class StartupUrlItem(Item):
    id = Field()
    link = Field()


class User(Item):
    startup_id = Field()
    startup_name = Field()
    user_id = Field()
    name = Field()
    headline = Field()
    url = Field()


def find_founder(member):
    if member['headline']:
        print(member['headline'])
        if re.search(rf'founder ?[\w]* ?{member['startup_name']}', member['headline'], re.IGNORECASE):
            return member['name']
    return None

class Startup(Item):
    id = Field()
    founders = Field(
        input_processor=MapCompose(find_founder),
        output_processor=Join(', ')
    )
    employee_range = Field(
        input_processor=MapCompose(lambda user: user['name']),
        output_processor=Join(', ')
    )
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
        input_processor=MapCompose(lambda value: value if value and value != '0' else None),
        output_processor=Join(' ')
    )
    location = Field()
    urls_social = Field(
        input_processor=MapCompose(str.strip, lambda value: value if value else None),
        output_processor=Join(', ')
    )
    description_short = Field()
    description = Field()


class StartupLoader(ItemLoader):
    default_output_processor = TakeFirst()