# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os


class SimilarPipeline(object):
    def process_item(self, item, spider):

        # 存在 , 去重
        if os.path.isfile(spider.file_name):
            with open(spider.file_name, "r") as rf:
                while True:
                    content = rf.readline()[:-1]
                    if content is None or content == "":
                        break

                    if item["word"] == content:
                        print("")
                        return item

        # 不存在 , 直接写入
        with open(spider.file_name, "a") as af:
            af.write(item["word"])
            af.write("\n")

        return item
