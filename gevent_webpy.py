"""A web.py apllication powered by gevent"""

from gevent import monkey;monkey.patch_all()
from gevent.pywsgi import WSGIServer
import time
import web

urls=("/","index",
      "/long","long_polling")

class index:
    def GET(self):
        return '<html>Hello,world!<br><a href="/long">/long</a></html>'

class long_polling:
    #Since gevent's WSGIServer executes each incoming connection in a separate greenlet
    #long running requests such as this one don't block one another;
    #and thanks to "moneky.patch_all()" statement at the top,thread-local storage used by web.ctx
    #becomes greenlet-local storage thus making requests isolated as they should be
    def GET(self):
        print "GET /long"
        time.sleep(10)#possible to block the request indefinitely,without harm others
        return 'Hello,10 seconds later'
def sessionyield_hotfix(func):
    def inner_generator(*args,**kwargs):
        ret=func.next()
        yield ret
    return inner_generator

s=None
s.session=None

class count1:
    @sessionyield_hotfix
    def GET(self):
        s.session.count+=1
        yield str(s.session.count)

class count_down:
    def GET(self,count):
        web.header('Content-type','text/html')
        web.header('Transfer-Encoding','chunked')
        yield '<h2>Prepare for Launch!</h2>'
        j='<li>Liftoff in %s...</li>'
        yield '<ul>'
        count=int(count)
        for i in range(count,0,-1):
            out=j%i
            time.sleep(1)
            yield out
        yield '</ul>'
        time.sleep(1)
        yield '<h1>Lift off</h1>'

class count_holder:
    def GET(self):
        web.header('Content-type','text/html')
        web.header('Transfer-Encoding','chunked')
        boxes=4
        delay=3
        countdown=10
        for i in range(boxes):
            output='<iframe src="/%d" width="200" height="500"></iframe>' %(countdown-i)
            yield output
            time.sleep(delay)

if __name__=="__main__":
    application=web.application(urls,globals()).wsgifunc()
    application.run()
    print "Serving on 8088..."
    WSGIServer(('',8080),application).serve_forever()