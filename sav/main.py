#!/usr/bin/python

import def_func_ServeurNetwork as ServeurNetwork
import def_func_LCD as LCD
import sys
import os
import time
import socket


# ====================================
# PROGRAMME PRINCIPAL
# ====================================

# Initialisation du serveur

Socket    = ServeurNetwork.InitConnexion()
Connexion = ServeurNetwork.WaitClient( Socket )

# Initialisation de l ecran LCD

lcd = LCD.Init()
lcd.clear()

cmdip = "ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"
lcd.message( "Welcome - F.Lavaud" )
lcd.message( 'IP %s' % (cmdip) )

# Attente d'un message reseau

while True :
	MsgClient = ServeurNetwork.ReadMsgClient( Connexion )

	print "Message recu sur client: ", MsgClient
	
	lcd.clear()
	lcd.message( MsgClient )
	
	if ( MsgClient == "FIN" ) :
		break

ServeurNetwork.Close( Connexion )
