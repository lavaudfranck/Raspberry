#!/usr/bin/python

# ====================================
# Variable globale
# ====================================

import VariableGlob as GLOB

import socket
import sys
import threading


# =====================================================
# Programme Reception
# =====================================================

class ThreadReception(threading.Thread):
#	"""objet thread gerant la reception des messages"""

	def __init__(self, nom ='' ):
		threading.Thread.__init__(self)
		self.connexion = nom           # ref. du socket de connexion
	
	def stop(self):
		self.Terminated = True
		threading.Thread.__stop__(self)

	def run(self):
		while 1:
			message_recu = self.connexion.recv(1024)
			print "SERVEUR MESSAGE> '%s" %message_recu + "'"
            
			if ( (message_recu =='') or (message_recu.upper() == "FIN") ) :
				break
            
        	# Le thread <reception> se termine ici.
        	# On force la fermeture du thread <emission> :
            
        	#	th_E._Thread__stop()
		self.Terminated = True
		self._Thread__stop()
		#self.Terminated = True
		#self.connexion._Thread__stop()
        	print "Client arrete."
        	self.connexion.close()
		print "Connexion fermee."


# =====================================================
# Programme Emission
# =====================================================

class ThreadEmission(threading.Thread):
#	"""objet thread gerant l'emission des messages"""
    
	def __init__(self, conn):
		threading.Thread.__init__(self)
		self.connexion = conn           # ref. du socket de connexion

	def run(self):
		while 1:
			message_emis = raw_input("Client message?")
			self.connexion.send(message_emis)


# ====================================
# Initialisation du Client
# Input  : aucune
# Output : socket
# ====================================


def InitClient() :
	
	connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		connexion.connect((GLOB.HOST, GLOB.PORT))
	except socket.error:
		print "La connexion a echoue."
		sys.exit()

	print "\n=> Connexion etablie avec le serveur <=\n"

	# Dialogue avec le serveur : on lance deux threads pour gerer
	# independamment l'emission et la reception des messages

	th_E = ThreadEmission(connexion)
	th_R = ThreadReception(connexion)

	th_E.start()
	th_R.start()

	return (th_E, th_R, connexion)
