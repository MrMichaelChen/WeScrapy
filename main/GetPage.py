# encoding:utf-8

import random
import os

from selenium import webdriver

from pachong.WeScrapy.Scrapybase.scrapybase import ScrapyBase
from monitor_func import monitor_timer
from pachong.WeScrapy.Scrapybase.scrapylog import logger
from pachong.WeScrapy.Scrapybase.sysconfig import scrapy_config


class ScrapyBaseHtml( ScrapyBase ):

    def find_flow_href(self, url):
        '''
        根据广度遍历，找到三层href的url
        :param url:
        :return:
        '''
        total_list = []
        depth_num = os.environ['depth_num']
        count = 0
        one_result_href_list = self.find_effect_href(url)
        total_list.extend(one_result_href_list)
        if one_result_href_list:
            while count < int(depth_num):
                for line in one_result_href_list:
                    if line not in total_list:
                        total_list.extend(self.find_effect_href(line))
                count += 1
        return total_list

    @monitor_timer
    def collect_num_page(self, url, num):
        '''
        进行广度遍历抓取页面html，num为随机个数,num为零是默认为全部网页
        :param url:
        :param num:
        :return:
        '''
        result_href = self.find_flow_href(url)
        result_html = {}
        print result_href
        if num < len(result_href):
            pass
        else:
            num = len(result_href)
        a = [random.randint(0, len(result_href)-1) for __ in range(num)]
        for line in a:
            try:
                result_html[str(result_href[line])] = self.get_whole_url_page(
                    result_href[line])
                logger.info(result_href[line] + " Finished!")
            except BaseException:
                result_html[str(result_href[line])] = self.get_ajax_page(
                    result_href[line])
                logger.info(result_href[line] + " Finished!")
            finally:
                pass
                # logger.info(result_href[line] + " Failed!")
        return result_html

    @monitor_timer
    def get_ajax_page(self, url):
        options = webdriver.ChromeOptions()
        options.add_argument(
            'user-agent="Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"')
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(url)

        html = driver.page_source
        return html

scrapy_base_html = ScrapyBaseHtml()

if __name__ == "__main__":
    aichen_url = "http://www.x-lab.ac:13000/#/index/course/experiment/35/1/0//cloudware"
    # print get_whole_url_page( url.strip( " " ) )
    url = 'https://mrmichaelchen.github.io/2018/05/23/Cisco-Orders/'
    sc = ScrapyBaseHtml()
    print sc.collect_num_page(url, 3)
    # print sc.get_ajax_page()
