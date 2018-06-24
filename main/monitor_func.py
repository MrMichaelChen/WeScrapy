# encoding=utf-8
import time
import psutil
import os
from functools import wraps


def monitor_timer(function):
    '''
    监控函数的执行时间
    :param function:
    :return:
    '''
    @wraps( function )
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function( *args, **kwargs )
        t1 = time.time()
        print 'Total time running %s: %s seconds' % (
            function.func_name, str( t1 - t0 ))
        return result

    return function_timer


class Monitor( object ):
    def __init__(self):
        pass

    def monitor_host(self):
        '''
        返回节点的物理信息
        :return:
        '''
        monitor_info = {}
        info = psutil.virtual_memory()
        free = str( round( psutil.virtual_memory().free / (1024.0 * 1024.0 * 1024.0), 2 ) )
        total = str( round( psutil.virtual_memory().total / (1024.0 * 1024.0 * 1024.0), 2 ) )
        memory = int( psutil.virtual_memory().total - psutil.virtual_memory().free ) / float(
            psutil.virtual_memory().total )
        # print u"物理内存： %s G" % total
        monitor_info['Physical memory'] = total
        # print u"剩余物理内存： %s G" % free
        monitor_info['Remaining physical memory'] = free
        # print u"物理内存使用率： %s %%" % int( memory * 100 )
        monitor_info['Physical memory usage'] = int( memory * 100 )
        # print u'内存使用：', psutil.Process(os.getpid()).memory_info().rss
        # print u'总内存：', info.total
        # print u'内存使用率：', info.percent
        # print u'cpu个数：', psutil.cpu_count()
        monitor_info['Cpu number'] = psutil.cpu_count()
        # print u'cpu物理核心', psutil.cpu_count(logical=False)
        monitor_info['Cpu physical core'] = psutil.cpu_count( logical=False )
        # print u'单个cpu使用率',psutil.cpu_percent(interval=1, percpu=True)
        cpu = (str)( psutil.cpu_percent( 1 ) ) + '%'
        # print u"cup使用率: %s" % cpu
        monitor_info['Cpu usage rate'] = cpu
        # print u'磁盘使用情况', psutil.disk_usage('/')  # 磁盘使用情况
        monitor_info['Disk usage'] = psutil.disk_usage( '/' )
        # print u'磁盘IO', psutil.disk_io_counters()  # 磁盘IO
        monitor_info['Disk IO'] = psutil.disk_io_counters()
        # print u'网络接口状态', psutil.net_if_stats()  # 获取网络接口状态
        monitor_info['Network interface status'] = psutil.net_if_stats()

        return monitor_info


if __name__ == '__main__':
    m = Monitor()
    print m.monitor_host()
