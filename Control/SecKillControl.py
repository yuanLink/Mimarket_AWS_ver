#   -*- coding:utf-8    -*-

from datetime import datetime, timedelta
import time
from Redis.RedisHandle import RedisHandle

class SecKillTrigger(object):
    """[TODO]: Add some decorator to trigger seckill main function
    """
    def __init__(self):
        self.on_sec_kill = False
        self.triggerTime = None
        self.triggerDuring = 4

    def begin_seckill(self):
        """ use this function to trigger seckill
        """
        self.triggerTime = datetime.now()
        self.on_sec_kill = True
        print("SEC KILL START AT {}".format(str(self.triggerTime)))

    def check_trigger(self):
        """ use this function to check if seckill start or finish
        BECAUSE NOW WE JUST TEST FOR THIS SOLUTION, THIS TRIGGER ONLY
        HAPPEN WITH 10 SEC 
        """
        # [TODO]: use real time to this trigger
        if datetime.now() - self.triggerTime > self.triggerDuring:
            return False
        return self.on_sec_kill

    def set_status(self,status):
        """ [TODO]:update trigger status with config/sql operation/sellout
        """
        self.on_sec_kill = status


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
        self.redis = RedisHandle()
        # [TODO]:Add Database Handle
        self.db = None
        self.config = Config()
        self.all_phone = self.config.get_phone_num()
        
    def init_connect(self):
        """ init redis and mysql handle
        [TODO]: read config file here
        """
        self.redis.connect_redis("localhost")
        # self.db

    def move_data_to_mysql(self):
        """ read all data from redis and write it into mysql
        BECAUSE WE DO NOT HAVE DISTRBUTED-VER, WE JUST USE 
        REDIS TO SYNCHRONIZE DATA
        """
        data_array = self.redis.get_all_data()
        buffer = []
        for each_phone in data_array:
            phone = each_phone[0]
            addr = each_phone[1]
            # [TODO]:write this into db
            print(each_phone)
            buffer.append(each_phone)
            # update all_phone
            self.all_phone -= 1
            if self.all_phone == 0:
                return False
        # now write buffer to database
        return True
    

trigger = SecKillTrigger()

def main():
    seckill_db = SecKillDBCommunication()
    trigger.begin_seckill()
    while trigger.check_trigger():
        # query redis_buffer and write into reids
        if not seckill_db.move_data_to_mysql():
            break
        time.sleep(0.01)

    trigger.set_status(False)


if __name__ == "__main__":
    # this module need to run utimaltely
   main() 