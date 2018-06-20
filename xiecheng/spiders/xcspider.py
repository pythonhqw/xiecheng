# -*- coding: utf-8 -*-
import scrapy

from xiecheng.items import XiechengItem


class XcspiderSpider(scrapy.Spider):
    name = 'xcspider'
    allowed_domains = ['hotels.ctrip.com']
    base_url = 'http://hotels.ctrip.com'
    start_urls = [base_url]

    def parse(self, response):
        city_list = response.xpath('//ul[@id="hotsold_city_list"]/li/a | //div[@id="pop_box_city"]/a')

        for city in city_list:

            if city.xpath("./@href").extract_first() == '###' or city.xpath("./@href").extract_first() == 'javascript:;':
                continue
            item = XiechengItem()
            item['city_link'] = self.base_url + city.xpath("./@href").extract_first()
            item['city_id'] = city.xpath("./@data-id").extract_first()
            item['city_name'] = city.xpath("./text()").extract_first()

            yield scrapy.Request(url=item['city_link'], meta={"item": item, "current_page": 1,
                                                              "show_page": 1}, callback=self.parse_city_one)

    def parse_city_one(self, response):
        if not response.meta['current_page'] != response.meta['show_page']:

            hotel_list = response.xpath('//div[@id="hotel_list"]/div/ul')[:-1]

            for hotel in hotel_list:
                item = response.meta['item']
                item['hotel_name'] = hotel.xpath('./li[2]/h2/a/text()').extract_first()
                item['hotel_score'] = hotel.xpath('./li[4]/div[1]/a/span[2]/text()').extract_first()
                item['hotel_price'] = hotel.xpath('./li[3]/div[1]/div/div/a/span/text()').extract_first()
                item['hotel_zone'] = hotel.xpath('./li[2]/p[1]/a[1]/text()').extract_first()
                item['hotel_link'] = self.base_url + hotel.xpath('./li[3]//a[@class="btn_buy"]/@href').extract_first()

                yield item

            next = response.request.url
            current_page = response.xpath("//a[@class='current']/text()").extract_first()
            show_page = response.xpath("//*[@id='txtpage']/@value").extract_first()
            page = int(show_page) + 1
            data = {'page': str(page)}

            yield scrapy.FormRequest(next, meta={"item": item, "current_page": current_page,
                                                 "show_page": show_page}, formdata=data,
                                     callback=self.parse_city_one, dont_filter=True)



