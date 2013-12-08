from tornado import gen
from tornado import options
import time,datetime
import tornado
def sync_loop_call(delta=60*1000):
    '''
    wait for func down then process add_timeout
    '''
    def wrap_loop(func):
        @wraps(func)
        @gen.coroutine
        def wrap_func(*args,**kwargs):
            options.logger.info("function %r start at %d" %(func.__name__,int(time.time())))
            try:
                yield func(*args,**kwargs)
            except Exception,e:
                options.logger.error("function %r error:%s" %(func.__name__,e))
            options.logger.info("function %r end at %d" % (func.__name__,int(time.time())))
            tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(milliseconds=delta),wrap_func)
        return wrap_func
    return wrap_loop

@sync_loop_call(delta=10*1000)
def worker():
    """
    do something
    """
    print 'well down,a good job'

if __name__=="__main__":
    worker()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

