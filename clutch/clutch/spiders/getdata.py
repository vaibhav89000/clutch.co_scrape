# -*- coding: utf-8 -*-
import scrapy
import time
import os
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import re
from ..items import ClutchItem

class GetdataSpider(scrapy.Spider):
    name = 'getdata'


    def start_requests(self):
        index = 0
        yield SeleniumRequest(
            url="https://clutch.co/directory/mobile-application-developers?sort_by=8&min_project_size=&avg_hrly_rate=&employees=&client_focus=&industry_focus=&location%5Bcountry%5D=GB&location%5Bcity%5D=&op=Apply&form_id=spm_exposed_form&form_build_id=form-0DFdfzD8_AClOwQAD2UxB2CwB0Vs7Z_inb_eZvpnYV4",
            wait_time=1000,
            screenshot=True,
            callback=self.parse,
            meta={'index': index},
            dont_filter=True
        )

    def parse(self, response):

        driver = response.meta['driver']
        html = driver.page_source
        response_obj = Selector(text=html)

        details = response_obj.xpath("//ul/li/div")
        # print('\n'*2)
        # print(details)
        # print('\n' * 2)
        clutchdetails_Item = ClutchItem()
        check = []
        for detail in details:
            name = detail.xpath(".//div[1]/div[1]/div/h3/a/text()").get()

            if(name != None):

                print('\n' * 2)
                # print(name)
                # print('\n' * 2)
                site_link = detail.xpath(".//div[2]/ul/li[1]/a/@href").get()
                print(name,site_link)
                check.append([name,site_link])
                count = site_link.count('/')
                if(count >= 3):
                     splitted = site_link.split('/')
                     # final_site = ''
                     # c = 0
                     # for splitsite in splitted:
                     #     if(c == 3):
                     #         break
                     #     c=c+1
                     print('\n' * 2)
                     print(splitted)
                     print('\n'*2)
                     if(len(splitted) > 2):
                         final_site = splitted[0] + '//' + splitted[2]
                         clutchdetails_Item['Company'] = name
                         clutchdetails_Item['Site'] = final_site
                     else:
                         clutchdetails_Item['Company'] = name
                         clutchdetails_Item['Site'] = site_link

                     yield clutchdetails_Item

                else:
                    clutchdetails_Item['Company'] = name
                    clutchdetails_Item['Site'] = site_link
                    yield clutchdetails_Item
                print('\n' * 2)
        print('\n'*2)
        print(len(check))
        print('\n' * 2)
