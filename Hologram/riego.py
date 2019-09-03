
from Hologram.HologramCloud import HologramCloud
from time import sleep, time, localtime, strftime
import datetime
import mpu3008
import urllib2
import RPi.GPIO as gpio

#Incluir GPIO Y sdev


#Hologram Setup
credentials = {'devicekey': '^hD8&#%H'} #Usar la Key de la SIM unica
cloud = HologramCloud(credentials, network='cellular', authentication_type='csrpsk')

#ThingSpeak setup
myAPI = "1C6E8L5UY683QB39" #Usar la API Key de escritura de ThingSpeak
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI

#Motor y gpio setup
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)             #Configuramos los pines GPIO como BCM
LED_PIN = 21  # #Como simbolo, el motor sera un LED
gpio.setup(LED_PIN, gpio.OUT) 
gpio.output(LED_PIN,True) #Led =1
led = 1
first = 1

global tiempo_inicial
tiempo_inicial = time()
tiempo_motor = 0
tiempo_parada = 0

rate_motor = 0.0000230555

#Tiempo
ciclo_1 = 5 #El programa duerme durante 1 hora para despues coger otra muestra

#Log_riego.txt
f1=open("/home/pi/Desktop/Hologram/log_riego.txt", "a+")

def send_message_to_thingspeak(menssage):
  try:
    f = urllib2.urlopen(baseURL+"&field1=%s"%(menssage))
    f.close()
  except:
    f1.write('Conexion fallida, intentando de nuevo...')

def get_agua_disponible_diaria():
  values_diarios_cada_mes = [0.07,0.06,0.06,0.07,0.44,0.45,0.44,2.86,4.16,1.73,1.79,0.69]
  d = datetime.date.today()
  return values_diarios_cada_mes[d.month - 1]



f1.write('Iniciando programa de riego...\n')

#sleep(5)

try:
  
  while True:
    if first== 1:
      first = 0
    else:
      if led == 1:
        tiempo_motor= tiempo_motor+ciclo_1
      else:
        tiempo_parada=tiempo_parada+ciclo_1
    
    d = datetime.datetime.now()
    if d.hour ==7 and d.minute >= 0 and d.minute <=59:
      tiempo_motor = 0
      tiempo_parada = 0
      led = 0
      gpio.output(LED_PIN,False)
      
    
    agua_disponible = get_agua_disponible_diaria()
    print agua_disponible
    porcentaje = mpu3008.get_water_percentage()
    send_message_to_thingspeak(porcentaje)
    cantidad_agua =tiempo_motor*rate_motor
    
    info =  " Agua utilizada: " + str(cantidad_agua) + " Litros  - " + "Humedad: " + str(porcentaje) + "%  - " + "Tiempo Motor: " + str(tiempo_motor) + " s  - Tiempo Parado: " + str(tiempo_parada) +" s\n" 
    
    timex = strftime("%d-%m-%Y %H:%M:%S", localtime()) + info
    f1.write(timex)
    
    #print info
    if porcentaje >= 50:
      gpio.output(LED_PIN,False)
      led = 0
      
    elif porcentaje <20:
      gpio.output(LED_PIN,True)
      led =1
      while porcentaje <30:
        sleep(ciclo_1)
        tiempo_motor= tiempo_motor+ciclo_1
        porcentaje = mpu3008.get_water_percentage()
        send_message_to_thingspeak(porcentaje)
        cantidad_agua = tiempo_motor*rate_motor
        
        info =  " Agua utilizada: " + str(cantidad_agua) + " Litros  - " + "Humedad: " + str(porcentaje) + "%  - " + "Tiempo Motor: " + str(tiempo_motor) + " s  - Tiempo Parado: " + str(tiempo_parada) +" s\n" 
        
        timex = strftime("%d-%m-%Y %H:%M:%S", localtime()) + info
        f1.write(timex)
        f1.flush()
    elif cantidad_agua < agua_disponible:
      led = 1
      gpio.output(LED_PIN,True)
    else:
      led = 0
      gpio.output(LED_PIN,False)
        
    sleep(ciclo_1)
    f1.flush()
    
except KeyboardInterrupt:   #Si el usuario pulsa CONTROL + C...
    print "\nFinalizando programa ....."  
    gpio.output(LED_PIN,False)
    gpio.cleanup()          #Limpiamos los pines GPIO y salimos
    f1.close()
    print "Terminado"
