import RPi.GPIO as GPIO    #Importamos la libreria GPIO
import time                #Importamos time
from time import gmtime, strftime  #importamos gmtime y strftime

from Hologram.HologramCloud import HologramCloud


GPIO.setmode(GPIO.BCM)             #Configuramos los pines GPIO como BCM
PIR_PIN = 17
GPIO.setup(PIR_PIN, GPIO.IN)       #Lo configuramos como entrada
 
#GPIO.setup(17, GPIO.OUT)          #Configuramos el pin 17 como salida (para un led)
 
 
hologram = HologramCloud(dict(), network='cellular')
print 'Cloud type: ' + str(hologram)

try:
    while True:  #Iniciamos un bucle infinito
        if GPIO.input(PIR_PIN): 
#           GPIO.output(17,True) #Encendemos el led
            time.sleep(0.5)        #Pausa de 1 segundo
            
            
            timex = strftime("%d-%m-%Y %H:%M:%S", gmtime()) #Creamos una cadena de texto con la hora
            timex = timex + " MOVIMIENTO DETECTADO"  #La sacamos por pantalla
            print timex
            time.sleep(1)  #Pausa de 1 segundo
            recv = hologram.sendMessage(timex,
                                topics = ['PIR_SENSOR'],
                                timeout = 3)
            print 'RESPONSE MESSAGE: ' + hologram.getResultString(recv)
#           GPIO.output(17,False)  #Apagamos el led
        time.sleep(1)              #Pausa de 1 segundo y vuelta a empezar
except KeyboardInterrupt:   #Si el usuario pulsa CONTROL + C...
    print "quit"            #Anunciamos que finalizamos el script
    GPIO.cleanup()          #Limpiamos los pines GPIO y salimos