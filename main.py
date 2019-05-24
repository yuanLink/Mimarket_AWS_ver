#   -*- coding:utf-8    -*-

import tornado.ioloop
import tornado.web
import os 
import json
import string
import urllib
from Control.BuyHandle import BuyHandle, BasicInfo
from Db.tables import Phone,User

g_buyHandler = BuyHandle()

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write("Hello world")
        # [TODO]: update global config in other module
        g_buyHandler.prepare_buy()
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
        # [TODO]: insert information with some trigger
        g_buyHandler.insert_buy_information(info)
        
        self.write("{status:success}")

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
if __name__ == "__main__":
    print("Entering main func")
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()

