#   -*- coding:utf-8    -*-

from Redis.RedisHandle import RedisHandle
import queue
import json


class BasicInfo(object):
    def __init__(self, addr, phone):
        self.phone = phone
        self.addr = addr

    def check_phone(self):
        if len(self.phone) != 11:
            return False

    def get_data(self):
        return (self.phone, self.addr)

    def __str__(self):
        return "Phone:{}, Addr:{}".format(self.phone,self.addr)


READY_FOR_REDIS = 10000

class BuyHandle(object):

    def __init__(self):
        self.phone_num = 0
        self.redisHandle = RedisHandle()
        self.infoQueue = queue.Queue(READY_FOR_REDIS)

    def prepare_buy(self):
        """ try to prepare for redis 
        """
        self.redisHandle.connect_redis()
        # [TODO] check return value

    def insert_buy_information(self, info):
        """ insert buying information from website
        info: Basic Information for phone and address

        Version 1. we use a simple queue, which we will
        insert all phone and address information, if this 
        queue is up to READY_FOR_REDIS, we will write to 
        reids
        """
        if self.infoQueue.full():
            multi_data = []
            while not self.infoQueue.empty():
                multi_data.append(self.infoQueue.get_nowait())

            self.redisHandle.set_multiple_data(multi_data)

        self.infoQueue.add(info.get_data())

    def fininsh_buy(self):
        """ insert last of data in queue into the redis
        """
        while not self.infoQueue.empty():
            multi_data.append(self.infoQueue.get_nowait())
        self.redisHandle.set_multiple_data(multi_data)



def testcase_buy_handle():

    testcase = []
    for i in range(1000):
        phone = str(i).zfill(6)
        addr = str(i)
        testcase.append((phone, addr))

    buyHandle = BuyHandle()
    buyHandle.prepare_buy()

    buyHandle.insert_buy_information(testcase)
    buyingHandle.fininsh_buy()



if __name__ == '__main__':
    buy = BuyHandle()
