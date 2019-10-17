import redis

class RedisQueue(object):
    """Simple Queue with Redis Backend"""
    def __init__(self, name, namespace='queue', **redis_kwargs):
        """The default connection parameters are: host='localhost', port=6379, db=0"""
        self.__db= redis.Redis(**redis_kwargs)
        self.key = '%s:%s' %(namespace, name)

    def qsize(self):
        """Return the approximate size of the queue."""
        return self.__db.llen(self.key)

    def empty(self):
        """Return True if the queue is empty, False otherwise."""
        return self.qsize() == 0

    def put(self, item):
        """Put item into the queue."""
        self.__db.rpush(self.key, item)

    def get(self, block=True, timeout=None):
        """Remove and return an item from the queue.

        If optional args block is true and timeout is None (the default), block
        if necessary until an item is available."""
        if block:
            item = self.__db.blpop(self.key, timeout=timeout)
        else:
            item = self.__db.lpop(self.key)

        if item:
            item = item[1]
        return item

    def get_nowait(self):
        """Equivalent to get(False)."""
        return self.get(False)


q = RedisQueue('test', password='Redis2019')
for j in range(10):
    print(q.put('hello world'))

for i in range(q.qsize()):
    print(q.get())

# create a connection to the localhost Redis server instance, by
# default it runs on port 6379
#redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, password="Redis2019")

# see what keys are in Redis
#print(redis_db.keys())
# output for keys() should be an empty list "[]"

#print(redis_db.set('full stack', 'python'))
# output should be "True"

#print(redis_db.keys())
# now we have one key so the output will be "[b'full stack']"

#print(redis_db.get('full stack'))
# output is "b'python'", the key and value still exist in Redis

#print(redis_db.incr('twilio'))
# output is "1", we just incremented even though the key did not
# previously exist

#print(redis_db.get('twilio'))
# output is "b'1'" again, since we just obtained the value from
# the existing key

#print(redis_db.delete('twilio'))
# output is "1" because the command was successful

#print(redis_db.get('twilio'))
# nothing is returned because the key and value no longer exist

