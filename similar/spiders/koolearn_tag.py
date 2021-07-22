import scrapy

from similar.spider_assist.items import WordItem
from similar.spiders import spider_name,file_name
import os


class KoolearnTagSpider(scrapy.Spider):
    name = spider_name

    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_name = file_name
    allowed_domains = ["www.koolearn.com/dict"]

    def start_requests(self):
        # 新东方在线

        # 四级核心词 分类记词汇表                          1-2
        # https://www.koolearn.com/dict/tag_936_{}.html

        # 扇贝循环单词书·四级核心词汇词汇表                 1-5
        # https://www.koolearn.com/dict/tag_938_{}.html

        # 四级考试大纲词表（2016版）词汇表                  1-25
        # https://www.koolearn.com/dict/tag_939_{}.html

        # 智能英语四级词汇书词汇表                          1-18
        # https://www.koolearn.com/dict/tag_940_{}.html

        # 大学英语课程教学要求积极词汇词汇表                 1-4
        # https://www.koolearn.com/dict/tag_941_{}.html

        # 四级高频词汇阅读分类词汇表                         1-4
        # https://www.koolearn.com/dict/tag_943_{}.html

        # 朗文当代英语辞典2000个核心注释词汇词汇表            1-9
        # https://www.koolearn.com/dict/tag_944_{}.html

        # 朗文当代英语高级词典最常用3000词汇词汇表            1-13
        # https://www.koolearn.com/dict/tag_945_{}.html

        url_format = "https://www.koolearn.com/dict/tag_{tag_index}_{page_index}.html"

        tag_index_list = [936, 938, 939, 940, 941, 943, 944, 945]
        page_index_range = range(1, 50)

        for tag_index in tag_index_list:
            for page_index in page_index_range:
                url = url_format.format(tag_index=tag_index, page_index=page_index)
                yield scrapy.Request(url=url, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1"},
                                     callback=self.parse)

    def parse(self, response):

        for word in response.xpath("//a[@class='word']/text()"):
            item = WordItem()
            item["word"] = word.extract()
            yield item
