from HTMLTags import *

import sys, urlparse
import threading

import sys
sys.path.insert( 0, '/home/pi/Projet_Elect/SpyCar2/' )

import os
import time
import socket

import VariableGlob as GLOB
import def_func_ClientNetwork as Fct


def StartClient() :
	#print "Recherche d'une connexion cliente sur ", GLOB.HOST + "<br>"
	th_e, th_r, connexion = Fct.InitClient()
	return connexion

def SendMessage( conn, msg ) :
	#print "ENVOIE DE LA COMMANDE BEAGLEBONE vers RASPBERRY : %s <br>" %msg
	conn.send( msg )
	return

def CloseClient( conn ) :
	#print "Deconnexion du client demande.<br>"
	SendMessage( conn, 'FIN')
	return


def foo(bar) :
	#print "===========================<br>"
	#print "Fonction foo activee:<br>"
	connexion = StartClient()
	#print "Commande a envoyer: '%s'" %bar + "<br>"
	SendMessage( connexion, bar )
	time.sleep( 0.1 )
	msg = "LCD:" + bar
	SendMessage( connexion, msg )
	time.sleep( 0.1 )
	SendMessage( connexion, "FIN" )
	#CloseClient( connexion )
	#print "==========================="
	raise HTTP_REDIRECTION,"http://192.168.0.41"
	return
