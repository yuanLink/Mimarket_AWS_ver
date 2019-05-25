#   -*- coding:utf-8    -*-

import tornado.ioloop
import tornado.web
import os 
import json
import string
import urllib
from Control.BuyHandle import BuyHandle, BasicInfo
from Control.SecKillControl import SecKillTrigger
from xmlrpc.client import ServerProxy
from Db.tables import Phone,User

# trigger_serv = ServerProxy("http://localhost:15000", allow_none=True)

class TriggerServQuery(object):
    def __init__(self):
        self.trigger_serv = ServerProxy("http://localhost:15000", allow_none=True)
        self.is_sec_kill = self.trigger_serv.check_trigger()

    def query_trigger(self):
        # [TODO]:Add Status before_sec, in_sec, after_sec
        # before_sec and in_sec will query every time bug
        # after_sec will not query just return false
        print("now self sec kill is {}".format(self.is_sec_kill))
        if self.is_sec_kill:
            self.is_sec_kill = self.trigger_serv.check_trigger()
        return self.is_sec_kill

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write("Hello world")
        # [TODO]: update global config in other module
        self.render("index.html")

class dbHandler(tornado.web.RequestHandler):
    retjson = {'code': '500', 'contents': 'unknown'}
    def post(self):
        user_phone = self.get_argument('User_phone', default='null')
        user_location = self.get_argument('User_location', default='null')
        # check
        phone = self.application.db.query(User).filter(User.User_phone == user_phone).one()
        if phone:
            self.retjson['code'] = '200'
            self.retjson['contents'] = u"this phone number has been used"
        else:
            new_user = User(
                User_phone=user_phone,
                User_location=user_location
            )
            self.application.db.merge(new_user)
            self.application.db.commit()
            self.retjson['code'] = '200'
            self.retjson['contents'] = 'success'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))
        '''
        if action == 'check': # get number of current
            phone_num = self.application.db.query(Phone).filter(Phone.phone_name == 'Xiaomi-9').one()
            self.retjson['code'] = 200
            self.retjson['contents'] = phone_num
        if action == 'modify':
            add_num = self.get_argument('add_num', default='1')
            phone_num = self.application.db.query(Phone).filter(Phone.phone_name == 'Xiaomi-9').one()
            add_num_ = string.atoi(add_num)
            phone_num += add_num_
            self.retjson['code'] = 200
            self.retjson['contents'] = phone_num
        '''

class MainHandler(tornado.web.RequestHandler):
    def deserialize_param(self, params):
        param_list = params.split("&")
        param_dict = {}
        for each_param in param_list:
            param_dict[each_param[:each_param.find("=")]] = urllib.parse.unquote(each_param[each_param.find("=")+1:])
        return param_dict

    def get(self):
        self.write("This handle must be resolve by post")

    def post(self):
        """ Save phone and address into redis
        """
        param = self.request.body.decode("utf-8")
        param = self.deserialize_param(param)
        # print(type(param))
        print(param)
        info = BasicInfo(param["address"], param["phone"])
        # [TODO]: insert information with some trgger\
        print("before checking...")
        try:
            if trigger_object.query_trigger():
                print("finish check")
                g_buyHandler.insert_buy_information(info)
                self.write("Sec kill success")
            else:
                self.write("The sec kill is finish")
                # g_buyHandler.last_buy()
        except ConnectionRefusedError as es:
            print("seckill finish")
            # g_buyHandler.last_buy()
            self.write("The sec kill is finish")


# Add new trigger to control buying

settings = {
    # "template_path": os.path.join(os.path.dirname(__file__), 'templates')
    'template_path': 'templates',
    "static_path": "static",
    "js_path": "js",
    "images_path": "images",
    "static_url_prefix": '/static/',
    "js_url_prefix": "/js/",
    "images_url_prefix": "/images/",
}

def make_app():
    return tornado.web.Application([
        (r"/", IndexHandler),
        (r"/buy", MainHandler)
    ], **settings)

# print("test")

trigger_object = TriggerServQuery()
g_buyHandler = BuyHandle()
g_buyHandler.prepare_buy()

if __name__ == "__main__":
    print("Entering main func")
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()

