import socket
import time 
from datetime import datetime 
from datetime import timedelta 
#netstat -na | Select-String "8080"

HOST = '192.168.1.145' # Enter IP or Hostname of your server
PORT = 12345 # Pick an open Port (1000+ recommended), must match the server port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))
reply = ''

def print_help():
	print "------------------------------------------------------------------------"
	print "\nOPCIONES:\n"
	print "1. rotacion"
	print "	   Imprime 5 veces la rotacion (en grados) en uno de los ejes del giroscopio. Cada dato se separa 1.5 segundos.\n"
	print "2. acceleracion"
	print "	   Imprime 5 veces la acceleracion (en m/s^2) en uno de los ejes del giroscopio. Cada dato se separa 1.5 segundos. \n"
	print "3. humedad"
	print "	   Imprime el valor de la humedad en el suelo en el momento\n"
	print "4. ambiente"
	print "	   Imprime los valores de temperatura y humedad en el ambiente\n"
	print "------------------------------------------------------------------------"
	
def rot_acc(socket_s, respuesta, modo):
	socket_s.send(modo)
	if modo = '1':
		titulo = 'ROTACION'
	else:
		titulo = 'ACCELERACION'
	
	eje = raw_input('Seleccione el eje (x, y, z): ')
	if eje == 'x':
		envio ='x'
	elif eje == 'y':
		envio = 'y'
	elif eje == 'z':
		envio = 'z'
	else:
		envio = 'None'
		
	if envio != 'None':
		socket_s.send(envio)
	
		print 'Transmitiendo informacion. Espere por favor, le llevara unos segundos.',
		tiempo = datetime.now()
		time.sleep(0.1)
		print'.........',
		time.sleep(0.2)
		print '................',
		time.sleep(0.1)
		print '......100%\n'
		i = 1
		while i<=2:
			longitud = socket_s.recv(1)
			#print longitud
			respuesta = socket_s.recv(int(longitud))
			print "TIME", tiempo.strftime("%d/%m/%Y, %H:%M:%S"), " - - - - "+ eje.capitalize() + " " + titulo + ": " + respuesta
			tiempo = tiempo + timedelta(seconds=1.5)
			i= i+1
		respuesta = 'OK'	
	else:
		print "Valor no valido. Anulando operacion"



#operaciones = { '0': ayuda, '1': rotacion}

#Lets loop awaiting for your input
while True:
	print reply + " hello"
	if reply == '' or reply == 'OK' or reply == 'Unknown command':
		seleccion = raw_input('Introduce el comando: (Escriba \'ayuda\' para ver todas las opciones) ')
		

	if seleccion == 'ayuda':
		print_help()
	elif seleccion == '1':
		rot_acc(s,reply,'1')
	elif seleccion == '2':
		rot_acc(s, reply, '2')
	elif seleccion == 'quit':
		s.send(seleccion)
		break
	else:
		s.send(seleccion)
	