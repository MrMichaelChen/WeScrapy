# encoding=utf-8
import requests,re
from bs4 import BeautifulSoup
from pachong.WeScrapy.Scrapybase.scrapylog import logger

class ScrapyBase( object ):
    headers = {'User-Agent': 'Mozilla/5.0'}
    def get_whole_url_page(self, url):
        '''
        抓取页面全部的html
        :param url:
        :return:
        '''
        try:
            r = requests.get(url,self.headers)
            bf1 = BeautifulSoup(r.content, "html.parser")
        except TypeError:
            bf1 = None
            exit(-1)
        return bf1

    def find_all_href(self, url):
        '''
        收集所有的href信息
        :param url:
        :return:
        '''
        href_list = []
        page_text = self.get_whole_url_page(url).prettify()
        if page_text:
            # res_str = r'<a.*?href=.*?>'
            res_href = r'<a.+?href=\"(.+?)\".*>'
            href_list = re.findall(res_href, page_text)
        return href_list

    def find_effect_href(self, url):
        '''
        过滤掉无效的href
        :param list:
        :return:
        '''
        effect_list = []
        list = self.find_all_href(url)
        if list:
            for line in list:
                try:
                    if requests.get(line):
                        effect_list.append(line)
                except BaseException:
                    pass
        else:
            logger.error("there is no href in the first page")
            exit(-1)
        return effect_list
