#!/usr/bin/env python3

import redis
from library import *

redis_host = "127.0.0.1"
redis_port = 6379
redis_password = ""
r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

class User(object):
	def __init__(self, uid, pseudo ) : 
		self.uid = uid 
		self.pseudo= pseudo 
		self.dico_friend = {}

	@property
	def uid(self):
		return self.__uid
	@uid.setter
	def uid(self, value):
		if not isinstance(value,str):
			try : 
				value = str(value)
		else :
			self.__uid = value 

	@property
	def pseudo(self):
		return self.__pseudo
	@pseudo.setter
	def pseudo(self, value):
		if not isinstance(value,str):
			try : 
				value = str(value)
		else :
			self.__pseudo= value 
	
		
	def addFriend(self,friend,etat):
		if not isinstance(friend,User):
			return False
		else : 
			self.dico_friend.update(friend,etat)
			return True 

	def getFriendRelation(self,friend):
		if not isinstance(friend,User):
			return None
		else : 
			for key in self.dico_friend :
				if key == friend :
					return self.dico_friend[key]
			return None 

	def updateFriendRelation(self,friend,newstatut):
		if not isinstance(friend,User):
			return False
		else : 
			for key in self.dico_friend :
				if key == friend :
					self.dico_friend[key] = newstatut
					return True
			
			return False 

