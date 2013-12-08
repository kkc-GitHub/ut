"""
LRU cache using redis
"""
from redis import StrictRedis as Redis

#settings
connection=Redis()
CACHE_SIZE=10000
POP_SIZE=200
CACHE_KEYS='lru-keys'
CACHE_STORE='lru-store'

def add_item(key,value):
    if not connection.hexists(CACHE_STORE,key):
        reorganize()
        connection.hset(CACHE_STORE,key,value)
        connection.zadd(CACHE_KEYS,0,key)

def reorganize():
    if connection.zcard(CACHE_KEYS)>=CACHE_SIZE:
        to_pop=connection.zrange(CACHE_KEYS,0,POP_SIZE)
        connection.zremrangebyrank(CACHE_KEYS,0,POP_SIZE)
        connection.hdel(CACHE_STORE,to_pop)

def get_item(key):
    result=connection.hget(CACHE_STORE,key)
    if result:#cache it
        connection.zincrby(CACHE_KEYS,key,1.0) #increment member for LRU
    return result

def test():
    """
    I can handle about 2800 keys/second (reads) and 7000 keys (writes)
    """
    from random import sample
    words=open('dict/wordlist.txt').readlines()[:10000]
    insert=sample(words,5000)

    for word in insert:
        add_item(word,word)

    search=sample(words,5000)
    for word in search:
        get_item(word)

if __name__=='__main__':
    test()