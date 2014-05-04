#!/usr/bin/python

# Auteur : F.Lavaud
# Carte : Raspberry Pi

# ====================================
# Variable globale
# ====================================

import VariableGlob as GLOB


# ====================================
# liste des imports
# ====================================

import sys
import socket
import os
import time
import def_func_LCD as LCD

import threading


# =====================================================
# Definition de la Class ThreadClient
# =====================================================

class ThreadClient( threading.Thread ):
	
	'''derivation d'un objet thread pour gerer la connexion avec un client'''
	
	def __init__( self, conn, ecrlcd ) :
		
		threading.Thread.__init__(self)
		self.connexion = conn
		self.ecranlcd  = ecrlcd

	def run(self) :
		
		# Dialogue avec le client :
		
		nom = self.getName()        # nom du thread
		ip  = GLOB.adresse[ nom ]   # adresse ip
			
		while 1:
			msgClient = self.connexion.recv(1024)
			print "MSG IN \t %15s" %ip + ":%10s" %nom + " \t '%s" %msgClient + "'"
            
			# Faire suivre le message a tous les autres clients
			
			for cle in GLOB.conn_client:
				if cle != nom and msgClient != "FIN" :      # ne pas le renvoyer a l emetteur
					ip2 = GLOB.adresse[ cle ]
					print "MSG OUT  %15s:%10s -> %15s:%10s \t '%s'" % (ip, nom, ip2, cle, msgClient)
					GLOB.conn_client[cle].send( msgClient )
            
			# Traite le message
			
			if ( ( msgClient == "FIN" ) or ( msgClient == "WEB_REBOOT" ) or ( msgClient == "WEB_SHUTDOWN" ) ) :
				break
			elif ( msgClient[0:3] == "LCD" ) :
				# Affiche sur l'ecran LCD le message recu
				self.ecranlcd = LCD.Init()
				self.ecranlcd.clear()
				#self.ecranlcd.message( 'Client say :\n' )
				self.ecranlcd.message( msgClient[4:] + '\n' )

		# Fermeture de la connexion
             	
		self.connexion.close()      		# couper la connexion cote serveur
		del GLOB.conn_client[nom]			# supprimer son entree dans le dictionnaire
		GLOB.NbrClient = GLOB.NbrClient - 1
		print "\nCLT OUT\t %15s tracked by %10s\n" % (GLOB.adresse[nom], nom)

		if ( msgClient == "WEB_REBOOT" ) :
			print "Reboot du systeme demande."
			self.ecranlcd.clear()
			self.ecranlcd.message( 'Reboot...\n' )
			os.system( "shutdown -r now" )
		elif ( msgClient == "WEB_SHUTDOWN" ) :
			print "Arret du systeme demande."
			self.ecranlcd.clear()
			self.ecranlcd.message( 'Shutdown...\n' )
			os.system( "shutdown -h now" )

		# Le thread se termine ici



# ====================================
# Initialisation du Serveur
# Input  : aucune
# Output : socket
# ====================================

def InitConnexion() :
	
	cmd   = "ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"
	GLOB.HOST = LCD.run_cmd( cmd )
	print "Lancement du serveur sur IP=", GLOB.HOST
    
	# creation du socket
	
	mySocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    
	# liaison du socket a une adresse precise
	
	try:
		mySocket.bind( ( GLOB.HOST, GLOB.PORT ) )
	except socket.error:
		print "La liaison du socket a l'adresse choisie a echoue."
		mySocket = 0
    	#sys.exit()

	return mySocket


# ====================================
# Initialisation du serveur - Mise en place du socket
# Input  : socket
# Output : it, connexion, adresse
# ====================================

def WaitNewClient( mySocket, ecran ) :
		
		# Attente de la requete de connexion d un client
    	##print "SERVEUR : Pret, en attente d'un client ..."
		
    	mySocket.listen( 5 )
	
    	# Etablissement de la connexion
    
    	connexion, adresse = mySocket.accept()
    	##print "SERVEUR : Client connecte, adresse IP %s, port %s" % ( adresse[0], adresse[1] )
        
    	# Creer un nouvel objet thread pour gerer la connexion
        
    	th = ThreadClient( connexion, ecran )
    	th.start()
        
    	# Memoriser la connexion dans le dictionnaire

    	it = th.getName()        # identifiant du thread
        GLOB.NbrClient = GLOB.NbrClient + 1
        GLOB.NameThread[ GLOB.NbrClient-1 ] = it
    	GLOB.conn_client[it]                = connexion
        GLOB.adresse[it]                    = adresse[0]
	GLOB.PThread[it]                    = th
    	##print "\n==> NEW CLIENT : %s connecte,  %s:%s <==" %(it, adresse[0], adresse[1])
        
    	# Dialogue avec le client
		
    	connexion.send("Vous etes connectes. Envoyez vos messages.")
    
	return it

