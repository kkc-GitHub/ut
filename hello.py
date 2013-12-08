import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado import escape
import json
from tornado.options import define,options
define("port",default=8000,help="run on the given port",type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        greeting=self.get_argument('greeting','Hello')
        self.write(greeting+',friendly user!')
class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        client=tornado.httpclient.AsyncHTTPClient()
        resp=yield client.fetch('https://api.github/users')
        if resp.code==200:
            resp=escape.json_decode(resp.body)
            self.write(json.dumps(resp,indent=4,separators=(',',':')))
        else:
            resp={"message":"error when fetch something"}
            self.write(json.dumps(resp,indent=4,separators={',',':'}))
        self.finish()
#a more detail for mainhandler
from tornado import gen
@gen.coroutine
def post(self):
    resp=yield GetUser()
    self.write(resp)
import logging
from tornado.httpclient import  AsyncHTTPClient
@gen.coroutine
def GetUser():
    client=AsyncHTTPClient()
    resp=yield client.fetch('https://api.github.com/users')
    if resp.code==200:
        resp=escape.json_decode(resp.body)
    else:
        resp={"message":"fetch client error"}
        logger.error("client fetch error %d,%s"%(resp.code,resp.message))
    raise gen.Return(resp)


if __name__=="__main__":
    tornado.options.parse_command_line()
    app=tornado.web.Application(handlers=[(r"/",IndexHandler)])
    http_server=tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

