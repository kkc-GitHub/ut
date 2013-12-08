import tornado.ioloop
from tornado.httpclient import AsyncHTTPClient

def callback(response):
    print response.body

def fetch():
    response=yield AsyncHTTPClient().fetch('http://justpic.org',callback)
    print response

gen=fetch()
gen.next()
try:
    gen.send('res')
except StopIteration:
    pass

tornado.ioloop.IOLoop.instance().start()