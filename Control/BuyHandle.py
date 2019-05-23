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
        # for each_info in info_array:
        #     # convert to tuple version
        #     self.infoQueue.put_nowait(each_info.get_data())
        #     if self.infoQueue.full():
        #         multi_data = []
        #         while not self.infoQueue.empty():
        #             multi_data.append(self.infoQueue.get_nowait())

        #         #  now the queue is empty
        #         self.redisHandle.set_multiple_data(multi_data)
        
        if self.infoQueue.full():
            multi_data = []
            while not self.infoQueue.empty():
                multi_data.append(self.infoQueue.get_nowait())

            #  now the queue is empty
            self.redisHandle.set_multiple_data(multi_data)
        
        self.infoQueue.put_nowait(info.get_data())
        # here we maybe last some data, we will call last_buy to finish it
        # print("[+] now we last {} element".format(self.infoQueue.qsize()))

    def last_buy(self):
        """ insert last of data in queue into the redis
        """
        multi_data = []
        while not self.infoQueue.empty():
            multi_data.append(self.infoQueue.get_nowait())
        self.redisHandle.set_multiple_data(multi_data)


    def check_data(self, phone_array):
        """ check data in redis
        phone_array the array of string saved phone

        if success, it will return data which save in redis
        """
        return self.redisHandle.get_multiple_data(phone_array)

    def finish_buy(self):
        """ finish buying control
        It will deal with some resource restore, and disclose redis
        """
        self.redisHandle.close_redis()



def testcase_buy_handle():

    testcase = []
    phonecase = []
    checkcase = []
    for i in range(1000):
        phone = str(i).zfill(6)
        addr = str(i)
        info = BasicInfo(addr, phone)
        testcase.append(info)
        phonecase.append(phone)
        checkcase.append(addr)

    buyHandle = BuyHandle()
    buyHandle.prepare_buy()

    # saving data in redis
    for each in testcase:
        buyHandle.insert_buy_information(each)
    # and we finish buying
    buyHandle.last_buy()

    # then we get data from redis to checkout it could save it
    pass_ = True
    tmp_case = buyHandle.check_data(phonecase)
    for check, tmp in zip(checkcase, tmp_case):
        if check != tmp.decode("utf-8"):
            print("[*] Error in get data testing:{}:{}".format(check, tmp))
            pass_ = False

    if pass_:
        print("[=] Test passed")
    # finally,end of this handle
    buyHandle.finish_buy()
    


if __name__ == '__main__':
    testcase_buy_handle()
