#!/usr/bin/pythonRoot
# bring in the libraries
import RPi.GPIO as G     
from flup.server.fcgi import WSGIServer 
import sys, urlparse
import time
import os
import threading

sys.path.insert( 0, '/home/pi/Projet_Elect/SpyCar2' )
import def_func_motor as Wheels
import def_func_ultrason as Ultrason
import def_func as fct


# Prepare les threads

a = fct.SetGoRandom( 'Thread A' )

def app(environ, start_response):

    # start our http response
    start_response("200 OK", [("Content-Type", "text/html")])
  
    # look for inputs on the URL
    i = urlparse.parse_qs(environ["QUERY_STRING"])
    yield ('&nbsp;') # flup expects a string to be returned from this function
        
    # if there's a url variable named 'q'
  
    speed = 100

    if "q" in i:
  
        if i["q"][0] == "uu" :
            Wheels.SetGo( 1, speed )
            time.sleep( 1. )
            Wheels.SetGo( 0, 0 )
  
        if i["q"][0] == "u" :
            Wheels.SetGo( 1, speed )
            time.sleep( 0.25 )
            Wheels.SetGo( 0, 0 )

        elif i["q"][0] == "l" :
            Wheels.SetGoAngle( -90 )

        elif i["q"][0] == "ll" :
            Wheels.SetGoAngle( -10 )

        elif i["q"][0] == "lll" :
            Wheels.SetGoAngle( -45 )

        elif i["q"][0] == "r" :
            Wheels.SetGoAngle( 90 )

        elif i["q"][0] == "rr" :
            Wheels.SetGoAngle( 10 )

        elif i["q"][0] == "rrr" :
            Wheels.SetGoAngle( 45 )

        elif i["q"][0] == "b" :
            Wheels.SetGo( -1, speed )
            time.sleep( 0.25 )
            Wheels.SetGo( 0, 0 )

        elif i["q"][0] == "bb" :
            Wheels.SetGo( -1, speed )
            time.sleep( 1. )
            Wheels.SetGo( 0, 0 )

        elif i["q"][0] == "s" :
            Wheels.SetGo(0,0)
        
        elif i["q"][0] == "q" :
            Wheels.SetGo(0,0)
            os.system( "shutdown -h now" )
        
        elif i["q"][0] == "restart" :
            Wheels.SetGo(0,0)
            os.system( "sudo service lighttpd restart" )

        elif i["q"][0] == "reboot" :
            Wheels.SetGo(0,0)
            os.system( "shutdown -r now" )

#       elif i["q"][0] == "dist" :
#           print "Take Distance"
#
#       elif i["q"][0] == "pict" :
#           print "Take Picture"
#
        elif i["q"][0] == "camOFF" :
            chaine = ""
            cmd    = os.popen( "ps -fu root | grep motion" )
            chaine = str( cmd.read() )
            id     = int( chaine[10:14] )
            chaine = "sudo killall -9 " + str( id )
            os.system( chaine )

        elif i["q"][0] == "camON" :
            chaine = "/opt/motion-mmal/motion -n -c '/opt/motion-mmal/motion-mmalcam.conf' &"
            os.system( chaine )
                
        elif i["q"][0] == "randomOFF" :
            Wheels.SetGo( -1, speed )
            time.sleep( 0.2 )
            Wheels.SetGo( 0, 0 )
            a.stop()
            Wheels.SetGo( 1, 0 )
            a.stop()
            Wheels.SetGo( 0, 0 )
            a.stop()
            Wheels.SetGo( 0, 0 )

        elif i["q"][0] == "randomON" :
            Wheels.SetGo( 1, speed )
            time.sleep( 0.2 )
            Wheels.SetGo( 0, 0 )
            a.__init__()
            a.start()


WSGIServer(app).run()
