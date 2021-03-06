# -*- coding: utf-8 -*-
import scrapy


class SpecialOffersSpider(scrapy.Spider):
    name = 'special_offers'
    allowed_domains = ['www.tinydeal.com']
    start_urls = ['https://www.tinydeal.com.hk/specials.html']

    def start_requests(self):
        yield scrapy.Request(url='https://www.tinydeal.com.hk/specials.html', callback=self.parse, headers={
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36 x-client-data: CIe2yQEIprbJAQjBtskBCKmdygEIy67KAQjQr8oBCLywygEIl7XKAQjttcoBCI66ygEI58bKAQiJx8oBGL66ygE="
        })

    def parse(self, response):
        for product in response.xpath("//ul[@class='productlisting-ul']/div/li"):
            yield {
                'title': product.xpath(".//a[@class='p_box_title']/text()").get(),
                'url': response.urljoin(product.xpath(".//a[@class='p_box_title']/@href").get()),
                'discounted_price': product.xpath(".//div[@class='p_box_price']/span[1]/text()").get(),
                'original_price': product.xpath(".//div[@class='p_box_price']/span[2]/text()").get(),
                "User-Agent":response.request.headers.get("User-Agent").decode("utf-8")
                # "User-Agent":response.request.headers['User-Agent']
            }
        
        next_page = response.xpath("//a[@class='nextPage']/@href").get()

        if next_page:
            # yield scrapy.Request(url=next_page,callback=self.parse,headers={
            #     'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36 x-client-data: CIe2yQEIprbJAQjBtskBCKmdygEIy67KAQjQr8oBCLywygEIl7XKAQjttcoBCI66ygEI58bKAQiJx8oBGL66ygE="
            # })
            yield scrapy.Request(url=next_page,callback=self.parse)
