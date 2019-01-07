#!/usr/bin/env python3

import redis
from library import *

redis_host = "127.0.0.1"
redis_port = 6379
redis_password = ""

def step1():
    try:
        r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
        exist = r.exists("compteur")
        if exist == 1:
            index = int(r.get("compteur"))
        else:
            index = 0
            r.set("compteur", index)
        pseudo = input("Rentrez votre username : ")
        found = existUsername(pseudo) # CHECK IF THE USERNAME EXISTS ALREADY IN THE DB
        while found == True:
        	print("{} est déjà pris.".format(pseudo))
        	pseudo = input("Essayez avec un autre : ")
        	found = existUsername(pseudo)
        usr = "user:" + str(index + 1)
        r.hset(usr, "UID", index + 1)
        r.hset(usr, "username", pseudo)
        r.hset(usr, "listeAmis", "")
        r.hset(usr, "requestAmis", "")
        r.incr("compteur")
        print(pseudo + " add")

    except Exception as e:
        print(e)

if __name__ == '__main__':
    step1()
