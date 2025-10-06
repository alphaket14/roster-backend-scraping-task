import scrapy


class ProfileItem(scrapy.Item):
    name = scrapy.Field()
    email = scrapy.Field()
    profile_link = scrapy.Field()
    role_type = scrapy.Field()
