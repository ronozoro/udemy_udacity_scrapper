# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UdacityItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    school_name = scrapy.Field()
    level = scrapy.Field()
    category = scrapy.Field()
    price = scrapy.Field()
    about = scrapy.Field()
    duration = scrapy.Field()
    prerequisites = scrapy.Field()
    instructors = scrapy.Field()
    skills = scrapy.Field()
    website = scrapy.Field()
    avg_rating = scrapy.Field()
    num_reviews = scrapy.Field()


class UdemyItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    is_paid = scrapy.Field()
    price = scrapy.Field()
    price_detail = scrapy.Field()
    price_serve_tracking_id = scrapy.Field()
    visible_instructors = scrapy.Field()
    published_title = scrapy.Field()
    tracking_id = scrapy.Field()
    description = scrapy.Field()
    head_line = scrapy.Field()
    num_subscribers = scrapy.Field()
    avg_rating = scrapy.Field()
    rating = scrapy.Field()
    status_label = scrapy.Field()
    instructional_level_simple = scrapy.Field()
    content_info = scrapy.Field()
    what_you_will_learn_data = scrapy.Field()
    prerequisites = scrapy.Field()
    objectives = scrapy.Field()
    target_audiences = scrapy.Field()
    course_has_labels = scrapy.Field()
    num_reviews = scrapy.Field()
