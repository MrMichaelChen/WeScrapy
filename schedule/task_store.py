# encoding = utf-8

from pachong.WeScrapy.connect.connector import create_connection


class Task_Store(object):
    receive_info = [[{'url':'www.baidu.com','num':'2','depth':'0','process':'0'}]]
    def __int__(self):
        pass

    def get_url(self):
        url_list = []
        for line in self.receive_info:
            url_list.append(url_list.append(self.receive_info[0]))
        return url_list

if __name__=="__main__":
    task = Task_Store()
    print task.get_url()