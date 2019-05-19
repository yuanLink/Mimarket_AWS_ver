import tornado.ioloop
import tornado.web
import os 
import json
import urllib

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write("Hello world")
        self.render("index.html")


class BuyHandler(tornado.web.RequestHandler):
	def deserialize_param(self, params):
		param_list = params.split("&")
		param_dict = {}
		for each_param in param_list:
			param_dict[each_param[:each_param.find("=")]] = urllib.parse.unquote(each_param[each_param.find("=")+1:])
		return param_dict

	def get(self):
		self.write("This handle must be resolve by post")

	def post(self):
		param = self.request.body.decode("utf-8")
		param = self.deserialize_param(param)
		# print(type(param))
		print(param)
		self.write("{status:success}")

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
        (r"/", MainHandler),
        (r"/buy", BuyHandler)
    ], **settings)

# print("test")
if __name__ == "__main__":
    print("Entering main func")
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()

