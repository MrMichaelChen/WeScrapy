# encoding=utf-8

import sys
import random
import json
import datetime

import os

from init_pro import ConnectionFactory, ConnectionProtocol, Connector
from twisted.internet import reactor, endpoints
from twisted.python import log
from twisted.web import xmlrpc, server
from pachong.WeScrapy.main.GetPage import scrapy_base_html
from pachong.WeScrapy.main.GetImage import scrapy_base_image
from pachong.WeScrapy.Scrapybase.sysconfig import scrapy_config
log.startLogging(sys.stdout)


class CreateConnection(object):

    def __init__(self, host, port):
        self.long_connection = ConnectionFactory(
            'ConnectionPlatform', ConnectionProtocol)
        self.long_connection.onlineProtocol = Connector
        self.host = host
        self.port = port
        self.status = False
        self.instance = None

    def create_long_connection(self):
        if not len(Connector.get_online_protocol('ConnectionPlatform')):
            print u"未连接.............."
            reactor.connectTCP(self.host, self.port, self.long_connection)
            print u'正在重连.............'
            self.status = False
            self.instance = None
        else:
            if self.status is False:
                self.instance = Connector.get_online_protocol(
                    'ConnectionPlatform')[0]
                self.status = True
                self.instance.transport.write(json.dumps(self.pack_data()))
                self.instance.work = None
                print u'已发送数据.............'
            else:
                if self.instance.work:
                    self.instance.work['schedule'] = 0.5
                    self.instance.work['entry_time'] = datetime.datetime.now(
                    ).strftime('%Y-%m-%d %H:%M:%S')
                    self.instance.work['status'] = 'work'
                    print self.instance.work['task_id'], "success"
                    self.instance.transport.write(
                        json.dumps(
                            scrapy_base_html.collect_num_page(
                                "https://mrmichaelchen.github.io/2018/05/23/Cisco-Orders/",
                                3)))
            reactor.callLater(1, self.create_long_connection)

    # @staticmethod
    # def pack_data():
    #
    #     info = dict()
    #     info["id"] = "1"
    #     info["weight"] = 50
    #     info["rpc_address"] = "127.0.0.1:5005"
    #     return info


# create_connection = CreateConnection('127.0.0.1', 5004)
create_connection = CreateConnection(
    str(os.environ['long_con_host']), int(os.environ['long_con_port']))
create_connection.create_long_connection()


class StateRpc(xmlrpc.XMLRPC):

    def xmlrpc_add_job(self, data):
        if create_connection.instance:
            create_connection.instance.work = data
            create_connection.instance.work_num += 1
            create_connection.instance.cur_weight = data['cur_weight']
            return {'status': 200}
        else:
            return {'status': 500, 'info': 'no master'}

    def xmlrpc_get_node_info(self):
        return {
            "memory_use": random.uniform(
                0,
                1),
            "memory_total": "15GB",
            "cpu_use": random.uniform(
                0,
                1),
            "cpu_total": "8个",
            "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "network_receive": "1.2M/s",
            "network_launch": "1.2M/s",
            "disk_use": random.uniform(
                0,
                1),
            "disk_total": "1000TB",
            "work_number": create_connection.instance.work_num,
            "cur_weight": create_connection.instance.cur_weight,
            "weight": create_connection.instance.weight}


rpc = StateRpc()
rpc_point = endpoints.TCP4ServerEndpoint(reactor, int(os.environ['rpc_port']))
rpc_point.listen(server.Site(rpc))

reactor.run()
