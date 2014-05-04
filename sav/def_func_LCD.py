#!/usr/bin/python

from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import * 
from time import sleep, strftime
from datetime import datetime

# ==========================================
# Initialisation de l ecran LCD
# Input  : aucune
# Output : lcd
# ==========================================
def Init() :

	lcd = Adafruit_CharLCD()
	lcd.begin(16,1)
	
	return lcd


def run_cmd( cmd ) :
	p = Popen( cmd, shell=True, stdout=PIPE )
	output = p.communicate()[0]
	
	return output
	
	
