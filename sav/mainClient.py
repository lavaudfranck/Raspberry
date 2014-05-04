#!/usr/bin/python

# Auteur : F.Lavaud
# Carte : Raspberry Pi

import def_func_ClientNetwork as ClientNetwork
import sys
import os
import time
import socket


# ====================================
# PROGRAMME PRINCIPAL
# ====================================

print "----------------------------------------------------------"

# Initialisation du client

Socket = ClientNetwork.InitConnexion()

while True :
	MsgClient = raw_input( "CLIENT : Votre message pour le serveur ? ")
	
	ClientNetwork.SendMsg( Socket, MsgClient )
	
	if ( MsgClient == "FIN" ) :
		break

ClientNetwork.Close( Socket )

print "---------------------------------------------------------"
