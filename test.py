#!/usr/bin/env python3

import redis
from library import *

redis_host = "127.0.0.1"
redis_port = 6379
redis_password = ""
r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

dico = {'2': '1', '3': '1', '4': '2'}



def printDico(dico):
	i = 0
	while i < len(dico):
		key = list(dico)[i]
		value = dico.get(key)
		print("{} : {}".format(key, value))
		i += 1

string = "1,1,2,3"

def str2dico(chaine):
	dico = {}
	i = 0
	while i < len(chaine): 
		dico[chaine[i]] = chaine[i+2]
		i += 4
	return dico

def str2list(chaine):
	tab = {}
	tab = chaine.split(',')
	return tab

print(str2dico(string))
print(len(str2dico(string)))