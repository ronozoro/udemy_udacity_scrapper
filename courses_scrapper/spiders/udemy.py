import json

import requests
from requests.auth import HTTPBasicAuth
from scrapy import Request
from scrapy import Spider
from scrapy.http import Response

from ..items import UdemyItem
from ..settings import CLIENT_SECRET, CLIENT_ID


class UdemySpider(Spider):
    name = "udemy_courses"
    start_url = 'https://www.udemy.com/api-2.0/courses/'

    def start_requests(self):
        yield Request(self.start_url, callback=self.parse_detail, dont_filter=True,
                      headers=requests.post(self.start_url,
                                            auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)).request.headers)

    def parse_detail(self, response: Response):
        data = json.loads(response.text)
        next = data.get('next')
        for record in data['results']:
            course = record
            item = UdemyItem()
            extra_filed = 'description,instructional_level_simple,content_info,what_you_will_learn_data,objectives,prerequisites,target_audiences,course_has_labels,num_subscribers,avg_rating,rating,num_reviews,status_label'
            extra_info = requests.get(
                'https://www.udemy.com/api-2.0/courses/{}/?fields[course]={}'.format(record['id'], extra_filed),
                auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)).json()
            item["title"] = course.get("title", None)
            item["url"] = 'https://www.udemy.com' + course.get("url", None)
            item["is_paid"] = course.get("is_paid", None)
            item["price"] = course.get("price", None)
            item["price_detail"] = course.get("price_detail", None)
            item["price_serve_tracking_id"] = course.get("price_serve_tracking_id", None)
            item["visible_instructors"] = course.get("visible_instructors", None)
            item["published_title"] = course.get("published_title", None)
            item["tracking_id"] = course.get("tracking_id", None)
            item["description"] = extra_info.get("description", None)
            item["head_line"] = course.get("headline", None)
            item["num_subscribers"] = extra_info.get("num_subscribers", None)
            item["avg_rating"] = extra_info.get("avg_rating", None)
            item["rating"] = extra_info.get("rating", None)
            item["status_label"] = extra_info.get("status_label", None)
            item["instructional_level_simple"] = extra_info.get("instructional_level_simple", None)
            item["content_info"] = extra_info.get("content_info", None)
            item["what_you_will_learn_data"] = extra_info.get("what_you_will_learn_data", None)
            item["prerequisites"] = extra_info.get("prerequisites", None)
            item["objectives"] = extra_info.get("objectives", None)
            item["target_audiences"] = extra_info.get("target_audiences", None)
            item["course_has_labels"] = extra_info.get("course_has_labels", None)
            item["num_reviews"] = extra_info.get("num_reviews", None)
            yield item
        if next:
            yield Request(next, callback=self.parse_detail, dont_filter=True, headers=requests.post(self.start_url,
                                                                                                    auth=HTTPBasicAuth(
                                                                                                        CLIENT_ID,
                                                                                                        CLIENT_SECRET)).request.headers)
