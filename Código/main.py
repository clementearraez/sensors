#!/usr/bin/env python2

from Hologram.HologramCloud import HologramCloud
from time import sleep, localtime, strftime
import urllib2
import gyro
import dueno
import smbus #Gyroscope
import RPi.GPIO as gpio

import random
import string

def getCoordinates():
    latitude = cloud.network.location.latitude
    longitude = cloud.network.location.longitude
    return latitude, longitude

def randomString(stringLength):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


#curl --verbose --request GET\'https://dashboard.hologram.io/api/1/users/me?apikey=RFJZbA2wy98MrHj6TIG9HyYAWQ6jR'
#GPIO
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)             #Configuramos los pines GPIO como BCM
PIR_PIN = 17  #PIR
gpio.setup(PIR_PIN, gpio.IN) 
gpio.setup(13, gpio.OUT) #Led de alarma

# Hologram Setup
credentials = {'devicekey': '^hD8&#%H'} # replace with your unique Sim device key
cloud = HologramCloud(credentials, network='cellular', authentication_type='csrpsk')

#Gyroscope

activo = 'A'
alerta = False

#cycleTime = 900 # this sets the refresh timer for the entire script - 900 for normal 15 minutes 

gsmLatitude = 0.0
gsmLongitude = 0.0
f1=open("/home/pi/Desktop/Hologram/alertas.txt", "a+")
f2=open("/home/pi/Desktop/Hologram/log_seguridad.txt", "a+")
#print 'Iniciando...'
#print "Sistema de seguridad activado"
        
#sleep(10) # lets allow a little time for the cellular interface to start - just in case :)
#startMsg = cloud.sendSMS("+34693608737", "Hello!! If you know Clemente, send him a Whatsapp! ;)")
# enter your mobile number in the space above, area code required
#sleep(60) # lets allow a little time for the cellular interface to restart
#print 'RESPONSE MESSAGE: ' + cloud.getResultString(startMsg)
    
#print baseURL
#sleep(1)

ciclo = 2
gpio.output(13,False)



try:   

#  if not cloud.network.is_connected():
#    result = cloud.network.connect()
#    if result == False:
#      print 'Failed to connect to cell network'
#    else:
#      print 'Connected to cell network'
  #response= 'Bienvenido al programa de seguridad. El sistema esta activado por defecto\n'
  #recv = cloud.sendMessage(response, topics = ['TRIGGER_SEGURIDAD'], timeout = 3)
  #print cloud.getResultString(recv)
  clave = randomString(5)
  mensaje_instruccion = "Bienvenido al programa de seguridad. Para activar el programa, envie primero la clave aleatoria. Su clave es: " + str(clave)
  print mensaje_instruccion
  recv = cloud.sendSMS("+14439044822", mensaje_instruccion)
  
  dueno.activar_sistema(cloud)

  while True:   
    sms = dueno.a_d_sms(cloud)
    #print sms
    if sms == 'D':
      activo = 'D'
      alerta = False
      ciclo = 2
      gpio.output(13,False)
      response = 'Sistema de seguridad desactivado'
      recv = cloud.sendMessage(response, topics = ['TRIGGER_DESACTIVAR'], timeout = 3)
      print cloud.getResultString(recv)
    elif sms == 'A':
      activo = 'A'
      response = 'Sistema de seguridad activado'
      recv = cloud.sendMessage(response, topics = ['TRIGGER_ACTIVAR'], timeout = 3)
      print cloud.getResultString(recv)
    #Si es 'U' se mantiene el valor de activo
    if alerta == True:
      ciclo = 10
      #print "Modo Alerta"
      gsmlatitude, gsmlongitude = getCoordinates()
      response = 'Coordenadas de la maquina: https://maps.google.com/maps?q=' + str(gsmlatitude) + ',' + str(gsmlongitude)
      recv = cloud.sendSMS("+14439044822", response)
      print recv
      #print response
      
      recv = cloud.sendMessage(response, topics = ['Location'], timeout = 3)
      #print 'RESPONSE MESSAGE: ' + cloud.getResultString(recv)
      
      (rot_x, rot_y) = gyro.rot_acc_all('r')
      (acc_x, acc_y) = gyro.rot_acc_all('a')
      rot = "Rotacion: " + str(rot_x) + " " + str(rot_y)
      ac = "Aceleracion: " + str(acc_x)+ " " + str(acc_y)
      timex = strftime("%d-%m-%Y %H:%M:%S", localtime()) #Creamos una cadena de texto con la hora
      rot = timex + " "+ rot + " " +ac +"\n"
      f2.write(rot)
      
    elif activo == 'A':
      if gpio.input(PIR_PIN):#Si detecta movimiento por cuerpo termico
        timex = strftime("%d-%m-%Y %H:%M:%S", localtime()) #Creamos una cadena de texto con la hora
        timex = timex + " MOVIMIENTO DETECTADO - Sensor PIR\n"  #La sacamos por pantalla
        #print timex
        f1.write(timex)
        f2.write(timex)
        recv = cloud.sendMessage(timex, topics = ['PIR_SENSOR'], timeout = 3)
        #print 'RESPONSE MESSAGE: ' + cloud.getResultString(recv)
        #INICIAR LED DE ALERTA!
        gpio.output(13,True)
        sleep(5)
        alerta = True
      else: #Utilizamos el giroscopio
        (rot_x, rot_y) = gyro.rot_acc_all('r') #Debe estar a 0 grados para no detectar robo, por lo tanto, se dejara un margen de 10 grados arriba y abajo.
        #Para estar seguros, se puede detectar movimiento en los ejes x, z. El y en este caso no se tendra en cuenta porque la maquina no subira a los cielos xD
        # 
        #0.017333984375 0.00244140625 0.97119140625 (ejex, eje y, eje z) cuando el gyro esta horizontal--> Ejemplo quieto. 
        #El eje z esta sometido a la fuerza gravitatoria de la tierra (9.8 m/s^2 = 1 g). Cuando el gyro este girado, el eje y tendra 1g, no nos hara falta.
        (acc_x, acc_y) = gyro.rot_acc_all('a')
        rot = "Rotacion: " + str(rot_x) + " " + str(rot_y)
        ac = "Aceleracion: " + str(acc_x)+ " " + str(acc_y)
        timex = strftime("%d-%m-%Y %H:%M:%S", localtime()) #Creamos una cadena de texto con la hora
        #print rot
        #print ac
        rot = timex + " - "+ rot + " - " +ac +"\n"
        f2.write(rot)
        
        if abs(rot_x)>8  or abs(rot_y) >8 or abs(acc_x) > 0.4 or abs(acc_y) >0.4:
          timex = timex + " Sospecha de Robo - Giroscopio\n"  #La sacamos por pantalla
          f1.write(timex)
          #print timex
          recv = cloud.sendMessage(timex, topics = ['GYRO_SENSOR'], timeout = 3)
          #print 'RESPONSE MESSAGE: ' + cloud.getResultString(recv)
          #INICIAR LED DE ALERTA!
          gpio.output(13,True)
          alerta = True             
             
    sleep(ciclo)  
    f1.flush()
    f2.flush()
   #SMSSent = 0 # latch to prevent SMS spam

except KeyboardInterrupt:   #Si el usuario pulsa CONTROL + C...
    #print "quit"            #Anunciamos que finalizamos el script
    f1.close()
    f2.close()
    gpio.cleanup()          #Limpiamos los pines GPIO y salimos