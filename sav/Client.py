#!/usr/bin/python

import socket
import os
import time

# ====================================
# Programme principal
# ====================================

HOST = '192.168.0.41'
PORT = 50000

# creation du socket
mySocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

# envoi d'une requete de connexion au serveur :
try:
    mySocket.connect( ( HOST, PORT ) )
except socket.error:
    print "La connexion a echoue."
    sys.exit()    
print "Connexion etablie avec le serveur."    

# Dialogue avec le serveur :
msgServeur = mySocket.recv(1024)

while True :
    if msgServeur.upper() == "FIN" or msgServeur =="":
        break
    print "S>", msgServeur
    msgClient = raw_input("C> ")
    mySocket.send(msgClient)
    msgServeur = mySocket.recv(1024)

# Fermeture de la connexion :
print "Connexion interrompue."
mySocket.close()
