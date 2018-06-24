# encoding=utf-8

import os
import time

import requests

from pachong.WeScrapy.Scrapybase.scrapybase import ScrapyBase
from monitor_func import monitor_timer
from pachong.WeScrapy.Scrapybase.scrapylog import logger


class ScrapyBaseImage( ScrapyBase ):
    folder_path = './image'

    def __init__(self):
        if os.path.exists(self.folder_path) == False:
            os.makedirs(self.folder_path)

    @monitor_timer
    def get_image(self, url):
        soup = self.get_whole_url_page(url)
        items = soup.find_all('img')

        for index, item in enumerate(items):
            try:
                if item:
                    html = requests.get(item.get('src'))
                    img_name = './'+self.folder_path +'/'+ str(index + 1) + '.png'
                    with open(img_name, 'wb') as file:
                        file.write(html.content)
                        # file.flush
                    file.close()
                    logger.info(item)
                    logger.info("GetImage程序：%d 下载完成" % (index + 1))
                    time.sleep(1)
            except BaseException:
                logger.info(item)
                logger.info("GetImage程序：%d 下载错误" % (index + 1))
                pass

scrapy_base_image = ScrapyBaseImage()

if __name__ == "__main__":
    # url = 'https://mrmichaelchen.github.io/2018/05/23/Cisco-Orders/'
    url = 'https://blog.csdn.net/Com_ma/article/details/79130734'
    sc = ScrapyBaseImage()
    sc.get_image(url)
