def h():
    #wen call next,this function can be run
    print 'wen chuan'
    #first next will hold here
    #next again ,5 will be the next value
    m=yield 5
    print 'first wait'
    print m
    print 'before second wait'
    #second next will hold here
    d=yield 12
    #next again,will continue follwing part
    print 'second wait'
    print d
    print 'we are together'
    #no hold place,it will throw a StopIteration

c=h()
q=c.next()
print q
q=c.send('well')
print q
q=c.send('bad')
print q
