import tornadoredis
import tornado.web
import tornado.gen

class RedisHandle():
	def __init__(self):
		self.client = tornadoredis.Client()

	def save_data(self, data):
		""" save data to redis
		@param: a format string that will save at redis
		"""
		with self.client.pipeline() as pipe:
			pipe.set()

