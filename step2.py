#!/usr/bin/env python3

import redis
from library import *

redis_host = "127.0.0.1"
redis_port = 6379
redis_password = ""

def step2():
    try:
        r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
        perso = input("Qui êtes-vous : ")
        if not(existUsername(perso)):
        	print("Vous ne passerez pas !")
        else:
	        pseudo = input("Ami à ajouter : ")
	        uidfriend = getUser(pseudo)
	        uidperso = getUser(perso)
	        if uidfriend != None and uidperso != None:
	        	usr = "user:" + str(uidfriend)
	        	chaineFriend = r.hget(usr, "listeAmis")
	        	chaineFriend += "," + uidperso
	        	r.hset(usr, "listeAmis", chaineFriend)
	        	print("add 1/2")
				usr = "user:" + str(uidpseudo)
	        	chainePerso = r.hget(usr, "listeAmis")
	        	chainePerso += "," + uidpseudo
	        	r.hset(usr, "listeAmis", chainePerso)
	        	print("add 2/2")

    except Exception as e:
        print(e)

if __name__ == '__main__':
    step2()