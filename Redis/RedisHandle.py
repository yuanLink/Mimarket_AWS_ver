#   -*- coding:utf-8    -*-

import asyncio
import aioredis
import numpy 

class RedisHandle(object):

    def __init__(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        # self.loop = asyncio.get_event_loop()
        self.redis = None

    async def __go_save_redis(self, key, data):
        await self.redis.set(key, data)
        # print("save data pair {}:{}".format(key, data))

    async def __go_save_multiple_data(self, tuple_array):
        for each_tuple in tuple_array:
            await self.redis.set(each_tuple[0], each_tuple[1])

    async def __go_get_redis(self, key):
        # print("get data {}".format(key))
        val = await self.redis.get(key)
        # print(val)
        return val

    async def __go_get_multiple_data(self, key_array):
        value_array = []
        for each_key in key_array:
            # print("try to get key {}".format(each_key))
            val = await self.redis.get(each_key)
            # print("get value {}".format(val))
            value_array.append(val)
        return value_array
        
    async def __close_connect_redis(self):
        self.redis.close()
        await self.redis.wait_closed()


    async def __connect_redis(self):
        # redis://host:6379/0?encoding=utf-8
        self.redis = await aioredis.create_redis_pool(
            'redis://localhost',
            minsize=5, maxsize=10,
            loop=self.loop
        )
        # print(self.redis)
    
    async def __go_get_all_keys(self):
        return await self.redis.keys("*")

    async def __go_get_all_data(self):
        data = []
        match = b"*"
        cur = b"0"
        while cur:
            cur, keys = await self.redis.scan(cur, match=match)
            for key in keys:
                tmp = await self.redis.get(key)
                data.append((key,tmp))
        return data

    def get_connect_redis(self):
        """ handle connection to redis
        """
        self.loop.run_until_complete(self.__connect_redis())

    def save_simple_data(self, key, data):
        """ save data to redis
        @param: a format string that will save at redis
        """
        self.loop.run_until_complete(self.__go_save_redis(key, data))

    def get_simple_data(self, key):
        """ get data from redis
        @param key: string for the key saving in redis

        if success, it will return data that saved in redis
        """
        val = self.loop.run_until_complete(self.__go_get_redis(key))
        return val

    def set_multiple_data(self, tuple_array):
        """ save multiple data 
        @param tuple_array: [(key, value)] for this array
        """
        self.loop.run_until_complete(self.__go_save_multiple_data(tuple_array))

    def get_multiple_data(self, key_array):
        """ get mutiple data
        @param key_array: ["key1", "key2" ...] for the key saving in database

        if success, it will return [b'value1', b'value2'...]
        """
        val_array = self.loop.run_until_complete(self.__go_get_multiple_data(key_array))
        return val_array

    def get_all_data(self):
        """ get all data from redis
        """
        task = self.loop.create_task(self.__go_get_all_data())
        val_array = self.loop.run_until_complete(task)
        # task.cancel()
        return val_array

    def connect_redis(self):
        """ connect redis
        """
        self.loop.run_until_complete(self.__connect_redis())

    def close_redis(self):
        """ close redis connection
        """
        self.loop.run_until_complete(self.__close_connect_redis())


def testcase_for_single_data():
    testcase = ("Value", "data")
    redisObj = RedisHandle()
    redisObj.connect_redis()
    redisObj.save_simple_data("Value", "data")
    val = redisObj.get_simple_data("Value")
    print(val)


def testcase_for_multiple_data(): 
    testcase = []
    for each in range(100):
        testcase.append(("test"+str(each), "value"+str(each)))

    keycase = [each_key[0] for each_key in testcase]
    redisObj = RedisHandle()
    redisObj.connect_redis()
    redisObj.set_multiple_data(testcase)
    valuecase = redisObj.get_multiple_data(keycase)
    assert(len(valuecase) == len(keycase))
    # print(valuecase)

    random_array = numpy.random.randint(len(testcase), size=len(testcase))
    for index in random_array:
        tmp_tuple = (keycase[index], valuecase[index].decode("utf-8"))
        if testcase[index] != tmp_tuple:
            print("[%d], testcase({}) != tmp_tuple({})".format(index, testcase[index], tmp_tuple))
            assert(0)

    print("[=] Test Pass[=]")

def testcase_for_all_data():
    testcase = []
    for each in range(100):
        testcase.append(("test"+str(each), "value"+str(each)))

    keycase = [each_key[0] for each_key in testcase]
    redisObj = RedisHandle()
    redisObj.connect_redis()
    redisObj.set_multiple_data(testcase)
    valuecase = redisObj.get_all_data()
    print(len(valuecase))
    print(len(keycase))
    assert(len(valuecase) == len(keycase))

    print(valuecase)
    redisObj.close_redis()

if __name__ == "__main__":

    # testcase_for_single_data()
    testcase_for_all_data()
    testcase_for_multiple_data()