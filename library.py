import redis

r = redis.StrictRedis(host="127.0.0.1", port=6379, password="", decode_responses=True)

def existUsername(pseudo):
	found = False
	i = 1
	#usr = "user:" + str(i)
	while r.hget("user:" + str(i), "username") != None and found == False:
		if r.hget("user:" + str(i), "username") == pseudo:
			found = True
			break
		else:
			i += 1
	return found

# fonction qui retourne l uid du pseudo 
def getUser(pseudo):
	if existUsername(pseudo):
		return getUID(pseudo)
	else: 
		return None

def getPseudo(uid):
	pseudo = r.hget("user:" + str(uid), "username")
	if pseudo != None:
		return pseudo
	else:
		print("Cet utilisateur n'existe pas.")

#retourne l'user d'un pseudo existant 
def getUID(pseudo):
	i = 1
	while r.hget("user:" + str(i), "username") != None:
		if r.hget("user:" + str(i), "username") == pseudo:
			return i
		else:
			i += 1
	return i # RETURN THE UID

def alreadyFriends(pseudo, pseudoFriend):
	alreadyFrd = False
	uidPerso = getUser(pseudo)
	uidFriend = getUser(pseudoFriend)
	if uidPerso != None:
		usr = "user:" + str(uid)
		AmisPerso = r.hget(usr, "listeAmis")
		listAmisPerso = str2list(AmisPerso)
		if uidFriend in listAmisPerso:
			print("Vous êtes déjà ami avec cette personne")
			alreadyFrd = True
			return alreadyFrd
		else:
			return alreadyFrd
	else:
		return None

def list2str(liste):
	chaine = ""
	i = 0
	for elem in liste:
		if i == len(liste) - 1:
			chaine += str(elem)
		else:
			chaine += str(elem) + ","
		i += 1
	return chaine

def str2dico(chaine):
	dico = {}
	i = 0
	while i < len(chaine): 
		#dico.update(chaine[i], chaine[i+2])
		dico[chaine[i]] = chaine[i+2]
		i += 4
	return dico

def dico2str(dico):
	chaine = ""
	i = 0
	for key in dico: 
		if i == len(dico) - 1:
			chaine += str(key) + "," + str(dico[key])
		else:
			chaine += str(key) + "," + str(dico[key]) + ","
		i += 1
	return chaine

