#!/usr/bin/env python3

# TODO
# Voir les status de ses amis

import redis
import time
from library import *

redis_host = "127.0.0.1"
redis_port = 6379
redis_password = ""
r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

# RELATIONS => (uid, i)
# i : typeDeRelations
#(0): n'existe pas
# 1 : Ami
# 2 : DemandeEnvoyee
# 3 : DemandeReçu

def wait(): # Sert à segmanter les tours afin d'améliorer la lisibilité durant le développement/test
	print("\nAppuyer sur une touche pour continuer\n")
	input()

def connexion():
	user_pseudo = input("Entrez votre pseudo : ")
	choice = None
	continuer = True
	while getUser(user_pseudo) == None and continuer == True:
		# while user doesnt exist 
		print("Introuvable")
		print("1. Créer un compte")
		print("2. Retenter")
		choice = input("Entrez votre choix : ")
		if choice == "1":
			# Créer compte
			continuer = False 
			return str(creer_compte()) 
		elif choice == "2":
			user_pseudo = input("Entrez votre pseudo : ")
	return str(getUser(user_pseudo))

def creer_compte():
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
	r.hset(usr, "relations", "")
	r.hset(usr, "statut", "")
	r.incr("compteur")
	print("Utilisateur {} créé !".format(pseudo))

	return r.hget(usr, "UID")

def dashboard(uidPerso):
	usr = "user:" + str(uidPerso)
	statut = r.hget(usr, "statut")
	if statut == "":
		statut = "Vous n'avez pas encore écrit de statut."
	pseudoPerso = getPseudo(uidPerso)
	strRelations = r.hget(usr, "relations")
	mesRelations = str2dico(strRelations)
	i = 0
	nbAmis = 0
	while i < len(mesRelations):
		key = list(mesRelations)[i]
		value = mesRelations.get(key)
		if value == "1":
			nbAmis += 1
		i += 1
	print("\n###############################\n")
	print("Bienvenue {}\n".format(pseudoPerso))
	print("Statut : {}".format(statut))
	print("Nombre d'amis : {}".format(nbAmis))
	print("\n###############################\n")

def menuPerso(uidPerso):
	pseudoPerso = getPseudo(uidPerso)
	dashboard(uidPerso)
	print("1. Voir vos notifications")
	print("2. Ajouter un ami")
	print("3. Supprimer un ami")
	print("4. Liste d'amis")
	print("5. Mettre à jour son statut")
	print("6. Voir le statut de ses amis.")
	print("7. Déconnexion / Retour au menu")

	connecte = True 
	choice = input("\nFaites votre choix : ")
	
	while connecte == True:
		if choice == "1": # Voir ses demandes d'ajouts
			# Affiche les notifications de l'user
			print("\n### NOTIFICATIONS ###\n")
			usr = "user:" + str(uidPerso)
			strRelations = r.hget(usr, "relations")
			mesRelations = str2dico(strRelations)
			i = 0
			notifs = False # To show if you have notifications or not
			while i < len(mesRelations):
				uid = str(list(mesRelations)[i])
				relations = mesRelations.get(uid)
				if relations == "3":
					notifs = True
					pseudoUID = getPseudo(uid)
					print("{} vous a envoyé une demande d'ami.".format(pseudoUID))
					ajouter = input("Accepter (Y / N) : ")
					if ajouter == "Y" or ajouter == "y":
						# On change le type de relation, on la passe en 'ami' désormais
						mesRelations[uid] = "1"
						strRelations = dico2str(mesRelations)
						r.hset(usr, "relations", strRelations)
						# 1/2

						# On ajoute la relation d'ami dans le champs 'relations' de l'ami
						usrFriend = "user:" + str(uid)
						strRelationsFriend = r.hget(usrFriend, "relations")
						RelationsFriend = str2dico(strRelationsFriend)
						RelationsFriend[uidPerso] = "1"
						strRelationsFriend = dico2str(RelationsFriend)
						r.hset(usrFriend, "relations", strRelationsFriend)
						# 2/2
						print("Vous êtes désormais amis.")
					elif ajouter == "N" or ajouter == "n":
						# On enlève l'invitation
						del mesRelations[uid]
						strRelations = dico2str(mesRelations)
						r.hset(usr, "relations", strRelations)
						# 1/2

						usrFriend = "user:" + str(uid)
						strRelationsFriend = r.hget(usrFriend, "relations")
						RelationsFriend = str2dico(strRelationsFriend)
						del RelationsFriend[uidPerso]
						strRelationsFriend = dico2str(RelationsFriend)
						r.hset(usrFriend, "relations", strRelationsFriend)
						print("Invitation refusée.")
				i += 1

			if notifs == False:
				print("Vous n'avez pas de notifications.")
			else:
				print("Vous n'avez plus de notifications.")

			connecte = False 
			menuPerso(uidPerso) # Notifications # Voir ses notifications
		elif choice == "2": # Cherche un user, l'ajoute (si aucune relation précédente) et envoie une request à l'user concerné
			pseudo = input("Ami à ajouter : ")
			uidFriend = getUser(pseudo)
			if uidFriend != None and uidPerso != None:
				# Put in a str the friends's list of myself
				usr = "user:" + str(uidPerso)
				strRelations = r.hget(usr, "relations") # on récupère sous forme de str notre liste d'amis
				mesRelations = str2dico(strRelations) # on transforme ce str en dico

				i = 0
				trouve = False
				while i < len(mesRelations):
					uid = list(mesRelations)[i]
					relations = mesRelations.get(uid)
					# Si l'UID du user est déjà dans la liste de mes relations
					if uid == str(uidFriend):
						if relations == "1":
							print("Vous êtes déjà amis.")
						elif relations == "2":
							print("Vous avez déjà envoyé une demande. En attente d'acceptation.")
						elif relations == "3":
							print("Il vous a envoyé une demande. En attente de votre approbation.\nAllez dans vos notifications.")
						else:
							print("")
						trouve = True
						#break
					i += 1

				# Si l'UID friend n'a pas été trouvé dans mes relations
				if trouve == False:
					# Envoie de l'invitation (côté perso)
					mesRelations[uidFriend] = "2" # On ajoute au dico l'UID de l'user ainsi que le statut "2" : une invitation a été envoyé
					strRelations = dico2str(mesRelations)
					r.hset(usr, "relations", strRelations)
					print("Invitation envoyée !")

					# Réception de l'invitation (côté friend)
					usrFriend = "user:" + str(uidFriend)
					strFriendRelations = r.hget(usrFriend, "relations")
					friendRelations = str2dico(strFriendRelations)
					friendRelations[uidPerso] = "3"
					strFriendRelations = dico2str(friendRelations)
					r.hset(usrFriend, "relations", strFriendRelations)
				
			else:
				print("Cet utilisateur n'existe pas.")
		
			connecte = False 		
			menuPerso(uidPerso)
		elif choice == "3": # Supprimer un ami
			pseudo = input("Ami à supprimer : ")
			uidFriend = getUser(pseudo)
			if uidFriend != None and uidPerso != None:
				# Commencer la suppression
				usr = "user:" + str(uidPerso)
				strRelations = r.hget(usr, "relations") # on récupère sous forme de str notre liste d'amis
				mesRelations = str2dico(strRelations) # on transforme ce str en dico

				i = 0
				while i < len(mesRelations):
					uid = list(mesRelations)[i]
					relations = mesRelations.get(uid)
					# Si l'UID du user est déjà dans la liste de mes relations
					if uid == str(uidFriend) and relations == "1":
						del mesRelations[uid]
						strRelations = dico2str(mesRelations)
						r.hset(usr, "relations", strRelations)
						# Delete 1/2

						usrFriend = "user:" + str(uid)
						strRelationsFriend = r.hget(usrFriend, "relations")
						RelationsFriend = str2dico(strRelationsFriend)
						del RelationsFriend[uidPerso]
						strRelationsFriend = dico2str(RelationsFriend)
						r.hset(usrFriend, "relations", strRelationsFriend)
						# Delete 2/2
						print("Ami supprimé.")
					i += 1
			else:
				print("Cet utilisateur n'existe pas.")
			connecte = False 		
			menuPerso(uidPerso)
		elif choice == "4": # Liste d'amis
			existeAmis = False
			usr = "user:" + str(uidPerso)
			strRelations = r.hget(usr, "relations")
			mesRelations = str2dico(strRelations)
			i = 0
			while i < len(mesRelations):
				key = list(mesRelations)[i]
				value = mesRelations.get(key)
				friend = getPseudo(key)
				if value == "1": # Ami
					print("Vous êtes ami avec {}.".format(friend))
					existeAmis = True
				elif value == "2":
					print("En attente d'acceptation de la part de {}.".format(friend))
				elif value == "3":
					print("Vous n'avez pas encore accepté {}.".format(friend))
				i += 1
			if existeAmis == False:
				print("Vous n'avez pas encore d'amis. Utilisez la fonction '2. Ajouter un ami' afin de retrouver vos connaissances.")
			connecte = False 		
			menuPerso(uidPerso)
		elif choice == "5": # Mettre à jour son statut
			usr = "user:" + str(uidPerso)
			post = str(input("Mettez à jour votre statut du moment : \n"))
			r.hset(usr, "statut", post)
			print("Statut modifié.")
			connecte = False
			menuPerso(uidPerso)
		elif choice == "6": # Voir le statut de ses amis
			nomAmi = input("Ami : ")
			uidAmi = getUser(nomAmi)
			if uidAmi != None and uidPerso != None:
				usr = "user:" + str(uidPerso)
				strRelations = r.hget(usr, "relations") # on récupère sous forme de str notre liste d'amis
				mesRelations = str2dico(strRelations) # on transforme ce str en dico

				i = 0
				while i < len(mesRelations):
					uid = list(mesRelations)[i]
					relations = mesRelations.get(uid)
					# Si l'UID du user est déjà dans la liste de mes relations
					if uid == str(uidAmi):
						if relations == "1": # Vous êtes amis, on peut avoir accès à son statut
							usrFriend = "user:" + str(uid)
							print("{} a posté : {}".format(nomAmi, r.hget(usrFriend, "statut")))
						else:
							print("Vous n'êtes pas amis avec {}.".format(nomAmi))
						i += 1

			else:
				print("Cet utilisateur n'existe pas.")
			connecte = False
			menuPerso(uidPerso)
		elif choice == "7": # Déconnexion | Retour au menu
			print("Vous êtes déconnecté.")
			connecte = False
			main() # Deconnexion / Retour au menu 
		else: 
			choice = input("Rentrez une instruction valable.\nFaites votre choix : ")

def main():
	choice = "0"
	quit = False
	
	while quit == False:
		print("\n##### MENU #####\n")
		print("1. Créer un compte")
		print("2. Se connecter")
		# print("3. Supprimer toutes les informations dans la base de données Redis (penser à remove ?)")
		print("(Q)uit.")

		choice = input("\nFaites un choix : ")

		if choice == "2":
			quit = True
			uidPerso = connexion()
			menuPerso(uidPerso)
			break 
		elif choice == "1":
			creer_compte()
		elif choice == "q" or choice == "Q":
			print("À la prochaine ! ")
			quit = True
		else:
			print("Rentrez une instruction valable.")

main()