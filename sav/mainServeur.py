#!/usr/bin/python

# ====================================
# Variable globale
# ====================================

import VariableGlob as GLOB


# ====================================
# liste des imports
# ====================================

import def_func_ServeurNetwork as ServeurNetwork
import def_func_LCD as LCD
import sys
import os
import time
import socket
import RPi.GPIO as GPIO

GPIO.setwarnings(False)


# ====================================
# PROGRAMME PRINCIPAL
# ====================================

print "\n---------------------------------"

# Initialisation de l ecran LCD

ecran = LCD.Init()
ecran.clear()

cmd   = "ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"
ligne = LCD.run_cmd( cmd )

ecran.message( "Bienvenue ...\n" )
ecran.message( 'IPs %s' % ligne )
time.sleep(5)

# Initialisation du serveur

GLOB.conn_client = {}                # dictionnaire des connexions clients
GLOB.adresse     = {}

iter   = 0
while True :
	iter = iter + 1
	Socket    = ServeurNetwork.InitConnexion()
	if ( Socket == 0 ) :
		ecran.clear()
		ecran.message( "Socket non dispo.\n" )
		ecran.message( "Try again %d" %iter )
		time.sleep(1)
	else :
		break
		
print "Serveur demarre avec succes."
ecran.clear()
ecran.message( "%s\n" % ligne )
ecran.message( "Wait IP Client..." )
time.sleep( 5 )

while True :
	it = ServeurNetwork.WaitNewClient( Socket )
	print "Client %s connecte (total=%d), adresse IP %s" %(it, GLOB.NbrClient, GLOB.adresse[it] )

	ecran.clear()
	ecran.message( "IP %s \n" %GLOB.adresse[it] )
	ecran.message( "Wait message ... \n")

	if GLOB.NbrClient < 0 :
		print "Arret volontaire du systeme"
		for i in -GLOB.NbrClient :
			print "\t --> Arret du thread %s" %NameThread[i]
			PThread[i]._Thread__stop()
		break

ecran.clear()
ecran.message( "Arret systeme\n" )
ecran.message( "Au revoir !" )

print "---------------------------------\n"
