import tornado.ioloop
from tornado.httpclient import  AsyncHTTPClient
import functools

def task(func,url):
    return functools.partial(func,url)

def callback(gen,response):
    try:
        gen.send(response)
    except StopIteration:
        pass

def sync(func):
    def wrapper():
        gen=func()
        f=gen.next()
        f(functools.partial(callback,gen))
    return wrapper()

@sync
def fetch():
    response=yield task(AsyncHTTPClient().fetch,'http://justpic.org')
    print '1'
    print response
    print '2'
fetch()
print '3'
tornado.ioloop.IOLoop.instance().start()