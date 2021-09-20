import json

from scrapy import Request
from scrapy import Spider
from scrapy.http import Response

from ..items import UdacityItem


class Udacity(Spider):
    name = "udacity_courses"
    start_url = "https://www.udacity.com/data/catalog.json"

    def start_requests(self):
        yield Request(self.start_url, callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response: Response):
        data = json.loads(response.text)
        for record in data:
            if record['type'] == 'course':
                course = record['payload']
                item = UdacityItem()
                item["name"] = course.get("title", None)
                item["url"] = "https://www.udacity.com{}".format(record['url'])
                item["school_name"] = course.get("school", None)
                item["level"] = course.get("level", None)
                item["category"] = 'Course' if course.get('nodeKey').startswith('ud') else 'nanodegree'
                item["price"] = round(((course.get('base_price_cents') or 0) / 100) * 16, 2)
                item["about"] = course.get("shortSummary", None)
                item["duration"] = course.get("displayDuration", None)
                item["prerequisites"] = course.get("prerequisites", None)
                item["skills"] = course.get("skills", None)
                item["website"] = 'Udacity'
                item["avg_rating"] = round((5 * course.get("ratingPercentage", 0)) / 100, 2)
                item["num_reviews"] = course.get("reviewCount", None)
                course_url = "https://www.udacity.com{}".format(record['url'])
                yield Request(course_url, callback=self.parse_course, dont_filter=True, meta={'item': item,
                                                                                              'nanodegree': False if course.get(
                                                                                                  'nodeKey').startswith(
                                                                                                  'ud') else True})

    def parse_course(self, response: Response):
        item = response.meta.get("item", UdacityItem())
        nanodegree = response.meta.get("nanodegree")
        if nanodegree:
            item["instructors"] = response.xpath(
                '/html/body/div[1]/div/div/div[2]/section[8]/div/div/div/div[1]/a/h5/text()').extract() \
                                  or response.xpath(
                '/html/body/div[1]/div/div/div[2]/section[7]/div/div/div/div[1]/a/h5/text()').extract()
        else:
            item["instructors"] = response.xpath(
                '/html/body/div[1]/div/div/div[2]/section[5]/section/div/div/div/h3/text()').extract() or \
                                  response.xpath(
                                      '/html/body/div[1]/div/div/div[2]/section[5]/div/div/div/div/a/h5/text()').extract()

        yield item
