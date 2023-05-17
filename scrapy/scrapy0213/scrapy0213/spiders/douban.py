import scrapy
from scrapy import Selector, Request
from scrapy.http import HtmlResponse

from scrapy0213.items import MovieItem


class BsrsSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["movie.douban.com"]
    # start_urls = ["https://movie.douban.com/top250"]

    def start_requests(self):
        """
        分析好链接，用这种方式可以少爬取一个页面，就是第一个页面
        会多爬取一次，因为定义start_urls与后面获取的href第一个不一样
        scrapy会认为这个页面没有爬取过。用这个方法就可以避免
        """
        for page in range(10):
            yield Request(url=f'https://movie.douban.com/top250?start={page*25}&filter=')

    def parse(self, response: HtmlResponse, **kwargs):
        sel = Selector(response)
        item_lists = sel.xpath('//*[@id="content"]/div/div[1]/ol/li')
        for item_list in item_lists:
            detail_url = item_list.xpath('./div/div[2]/div[1]/a/@href').extract_first()
            print(detail_url)
            #定义管道处理的对象
            movie_item = MovieItem()
            #extract_first() 获取sel对象第一个内容，并接收到item里
            movie_item['title'] = item_list.xpath('./div/div[2]/div[1]/a/span[1]/text()').extract_first()
            movie_item['rank'] = item_list.xpath('./div/div[2]/div[2]/div/span[2]/text()').extract_first()
            movie_item['subject'] = item_list.xpath('./div/div[2]/div[2]/p[2]/span/text()').extract_first()
            yield Request(
                url=detail_url, callback=self.parse_detail,
                cb_kwargs={'item': movie_item}
            )

        # #start_urls是类属性。这种要会，但不是最优
        # hrefs_list = sel.xpath('//*[@id="content"]/div/div[1]/div[2]/a/@href')
        # for href in hrefs_list:
        #     #选择器列表可以用extract_first()，单个选择器对象后面没有继续xpath用extract()
        #     #urljoin用来拼接完整的url，需要导入HtmlResponse并在parse中指定response类型
        #     url = response.urljoin(href.extract())
        #     yield Request(url=url)

    def parse_detail(self, response, **kwargs):
        sel = Selector(response)
        movie_item = kwargs['item']
        movie_item['duration'] = ''
        print(movie_item)
        yield movie_item

