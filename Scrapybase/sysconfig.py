import ConfigParser
import os
from scrapylog import logger


class SysConfig( object ):
    cf = ConfigParser.ConfigParser()

    def __init__(self):
        pass

    def read_sysconfig(self):
        if os.path.exists("../Scrapyconfig/sysconfig.conf"):
            try:
                self.cf.read("../Scrapyconfig/sysconfig.conf")
                os.environ['rpc_host'] = self.cf.get("rpc_config", "host")
                os.environ['rpc_port'] = self.cf.get("rpc_config", "port")
                os.environ['depth_num'] = self.cf.get(
                    "scrapy_depth", "depth_num")
                os.environ['long_con_host'] = self.cf.get("long_con_config","host")
                os.environ['long_con_port'] = self.cf.get("long_con_config","port")
            except Exception as e:
                logger.error(e)
                exit(-1)
        else:
            logger.error("Missing configuration file sysconfig.conf !")
            exit(-1)
        return


scrapy_config = SysConfig()
scrapy_config.read_sysconfig()
