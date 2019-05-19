import tornado.ioloop
import tornado.web
import os 

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write("Hello world")
        self.render("index.html")

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
    ], **settings)

# print("test")
if __name__ == "__main__":
    print("Entering main func")
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()

