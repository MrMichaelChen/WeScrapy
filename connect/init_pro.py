# encoding=utf-8
import re
import json
from twisted.internet.protocol import ClientFactory, Protocol


class ConnectionFactory(ClientFactory):
    def __init__(self, name=None, protocol=None):
        self.instanceFactoryName = name
        self.protocol = protocol
        self.numProtocols = 0
        self.onlineProtocol = None

        print self.instanceFactoryName + 'Client start connecting'
        return


class ConnectionProtocol(Protocol):
    def __int__(self):
        self.div_name = ""
        self.status = False

    def connectionMade(self):
        self.factory.numProtocols += 1
        self.div_name = 'ConnectionPlatform'
        print "Connection successful, the current number of ConnectionPlatform is" + \
            str(self.factory.numProtocols)
        self.factory.onlineProtocol.add_client(self.div_name, self)
        self.status = True

    def connectionLost(self, reason=""):
        if self.status:
            print "the reason of ConnectionPlatform lost is" + \
                str(reason) + "\n"
            self.factory.numProtocols -= 1
            print "the current number of ConnnectionPlatform is " + \
                str(self.factory.numProtocols) + "\n"
            self.factory.onlineProtocol.del_client(self.div_name)
            self.status = False
        else:
            pass

    def dataReceived(self, data):
        try:
            print data
            json_data = json.loads(data)
            if json_data['status'] == 200:
                print "success"
            elif json_data['status'] == 404:
                print "not found"
            elif json_data['status'] == 403:
                self.connectionLost("node existed!")
            else:
                self.connectionLost("some thing error")
        except Exception as e:
            print e


class Connector(object):
    def __init__(self):
        self.online_protocol = {}

    def get_online_protocol(self, div_name):
        protocol_list = []
        pattern = re.compile(div_name)
        for i in self.online_protocol.keys():
            if pattern.match(i):
                protocol_list.append(self.online_protocol.get(i))
        return protocol_list

    def add_client(self, div_name, host):
        self.online_protocol[div_name] = host
        print "add" + div_name + "after, the current equipment is " + \
            str(self.online_protocol)
        print "\n"

    def del_client(self, div_name):

        if self.online_protocol.get(div_name):
            print "you want to delete " + div_name
            del self.online_protocol[div_name]
        else:
            print "Not Found the div you want to delete!"

        print "Delete " + div_name + \
            "after,the current equipment is " + str(self.online_protocol)

Connector = Connector()