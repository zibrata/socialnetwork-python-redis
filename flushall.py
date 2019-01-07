#!/usr/bin/env python3

# step 1: import the redis-py client package
import redis

# step 2: define our connection information for Redis
# Replaces with your configuration information
redis_host = "127.0.0.1"
redis_port = 6379
redis_password = ""

def hello_redis():
    try:

        r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
        r.flushall();

    except Exception as e:
        print(e)

if __name__ == '__main__':
    hello_redis()
