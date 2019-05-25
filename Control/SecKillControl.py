#   -*- coding:utf-8    -*-

from datetime import datetime, timedelta
from xmlrpc.server import SimpleXMLRPCServer
from Redis.RedisHandle import RedisHandle
import threading
import time
import asyncio

class SecKillTrigger(object):
    """[TODO]: Add some decorator to trigger seckill main function
    Add RPC calling so sec kill could be called by remote
    """
    _rpc_methods_ = ['check_trigger', 'set_status']
    def __init__(self, addr):
        """  init basical tool
        addr:(ip, port) of this server
        """
        loop = asyncio.get_event_loop()
        self.redis = RedisHandle(loop)
        self.on_sec_kill = False
        self.triggerTime = None
        self.triggerDuring = 3000
        self.__serv = SimpleXMLRPCServer(addr, allow_none=True)
        for name in self._rpc_methods_:
            self.__serv.register_function(getattr(self, name))

    def begin_seckill(self):
        """ use this function to trigger seckill
        """
        self.triggerTime = datetime.now()
        # self.redis.connect_redis("localhost")
        # self.redis.save_simple_data("SEC_KILL","START")
        self.on_sec_kill = True
        print("SEC KILL START AT {}".format(str(self.triggerTime)))

    def check_trigger(self):
        """ use this function to check if seckill start or finish
        BECAUSE NOW WE JUST TEST FOR THIS SOLUTION, THIS TRIGGER ONLY
        HAPPEN WITH 10 SEC 
        """
        # [TODO]: use real time to this trigger
        # print("check data {}".format((datetime.now() - self.triggerTime).seconds))
        if (datetime.now() - self.triggerTime).seconds > self.triggerDuring:
            # print("finish")
            self.on_sec_kill = False
        return self.on_sec_kill

    def update_trigger(self):
        # print((datetime.now() - self.triggerTime).seconds)
        if (datetime.now() - self.triggerTime).seconds > self.triggerDuring:
            self.set_status(False)

    def set_status(self, status):
        """ [TODO]:update trigger status with config/sql operation/sellout
        """
        self.on_sec_kill = status
        # if status == False:
        #     self.redis.save_simple_data("SEC_KILL","END")
        # else:
        #     self.redis.save_simple_data("SEC_KILL","START")

    def serve_forever(self):
        while self.on_sec_kill:
            self.__serv.handle_request()
        # handle the final one
        self.__serv.handle_request()
        print("RPC Finish")
        return
        


PHONE_NUM = 1000000

class Config(object):
    """ This object will record the real data 
    from config file
    """
    def __init__(self):
        self.phone_num = PHONE_NUM

    def get_phone_num(self):
        return self.phone_num

class SecKillDBCommunication(object):
    def __init__(self):
        loop = asyncio.get_event_loop()
        self.redis = RedisHandle(loop)
        # [TODO]:Add Database Handle
        self.db = None
        self.config = Config()
        self.all_phone = self.config.get_phone_num()
        
    def init_connect(self, url):
        """ init redis and mysql handle
        @param url: the target redis url

        [TODO]: read config file here
        """
        self.redis.connect_redis(url)
        # self.db

    def move_data_to_mysql(self):
        """ read all data from redis and write it into mysql
        BECAUSE WE DO NOT HAVE DISTRBUTED-VER, WE JUST USE 
        REDIS TO SYNCHRONIZE DATA
        """
        # print("move data....")
        data_array = self.redis.get_all_data()
        buffer = []
        ret = True
        for each_phone in data_array:
            phone = each_phone[1]
            addr = each_phone[0]
            # [TODO]:write this into db
            print(each_phone)
            buffer.append(each_phone)
            # update all_phone
            self.all_phone -= 1
            if self.all_phone == 0:
                ret = False
        # now write buffer to database
        self.redis.clear_data()
        return ret
    

# trigger = SecKillTrigger()

def testcase_for_SeckKillDBCommunication():
    seckill_db = SecKillDBCommunication()
    seckill_db.init_connect("localhost")
    seckill_db.move_data_to_mysql()

def main():
    trigger = SecKillTrigger(("",15000))
    seckill_db = SecKillDBCommunication()
    seckill_db.init_connect("localhost")
    
    trigger.begin_seckill()
    t1 = threading.Thread(target=trigger.serve_forever)
    t1.setDaemon(True)
    t1.start()
    while trigger.check_trigger():
        # query redis_buffer and write into reids
        if not seckill_db.move_data_to_mysql():
            break
        time.sleep(0.01)
        trigger.update_trigger()

    trigger.set_status(False)
    print("Finish the Seckill")


if __name__ == "__main__":
    # this module need to run utimaltely
   main()