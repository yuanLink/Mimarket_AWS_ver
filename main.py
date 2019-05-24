#   -*- coding:utf-8    -*-

import tornado.ioloop
import tornado.web
import os 
import json
import urllib
from Db import *
from Control.BuyHandle import BuyHandle, BasicInfo
from Control.SecKillControl import SecKillTrigger
from xmlrpc.client import ServerProxy

g_buyHandler = BuyHandle()
trigger_serv = ServerProxy("http://localhost:15000", allow_none=True)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write("Hello world")
        # [TODO]: update global config in other module
        g_buyHandler.prepare_buy()
        self.render("index.html")


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
            if trigger_serv.check_trigger():
                print("finish check")
                g_buyHandler.insert_buy_information(info)
                self.write("Sec kill success")
            else:
                g_buyHandler.last_buy()
                self.write("The sec kill is finish")
        except ConnectionRefusedError as es:
            print("check finish")
            g_buyHandler.last_buy()
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
if __name__ == "__main__":
    print("Entering main func")
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()

