from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from similar.spiders import spider_name

if __name__ == '__main__':

    spider_list = [spider_name]  # , "koolearn_cet4_core", "koolearn_tag_938"]

    spider_crawler = []
    settings = get_project_settings()

    crawler = CrawlerProcess(settings)

    for spider_name in spider_list:
        crawler.crawl(spider_name)

    crawler.start()
