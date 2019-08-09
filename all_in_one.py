#All in one. Including the TCP connection and all the sensors

#!/usr/bin/python
#netstat -na | grep "8080"
#https://www.cyberciti.biz/faq/linux-command-forcibly-close-socket-ports-in-time_wait-state/
#Invoke-RestMethod ipinfo.io/ip
#irm ipinfo.io/ip 
import socket #TCP connections
import smbus #Gyroscope
import math
import time



def read_byte(reg):
    return bus.read_byte_data(address, reg)

def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value

def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

def get_z_rotation(x,y,z):
    radians = math.atan2(z, dist(x,y))
    return math.degrees(radians)

def rot_acc(axis, mode):
    gyroskop_xout = read_word_2c(0x43)
    gyroskop_yout = read_word_2c(0x45)
    gyroskop_zout = read_word_2c(0x47)
    speed_xout = read_word_2c(0x3b)
    speed_yout = read_word_2c(0x3d)
    speed_zout = read_word_2c(0x3f)
    speed_xout_scalated = speed_xout / 16384.0
    speed_yout_scalated = speed_yout / 16384.0
    speed_zout_scalated = speed_zout / 16384.0
    if mode == 'r':
      if axis == 'x':
        return str(round(float(get_x_rotation(speed_xout_scalated, speed_yout_scalated, speed_zout_scalated)),3))
      elif axis == 'y':
        return str(round(float(get_y_rotation(speed_xout_scalated, speed_yout_scalated, speed_zout_scalated)),3))
      elif axis == 'z':
        return str(round(float(get_z_rotation(speed_xout_scalated, speed_yout_scalated, speed_zout_scalated)),3))
    elif mode == 'a':
      if axis == 'x':
        return str(round(speed_xout_scalated,3))
      elif axis == 'y':
        return str(round(speed_yout_scalated,3))
      elif axis == 'z':
        return str(round(speed_zout_scalated,3))

def get_five_rot_acc(letter, modo):
    array_num = ["hola"]
    array_num[0] = rot_acc(letter, modo)
    count = 0
    while count <3:
      time.sleep(1.75)
      array_num.append(rot_acc(letter, modo))
      count = count +1
    return array_num


def comando_rotaciones_aceleraciones(socket_s, palabra,modo,respuesta):
    print 'Mandando info'
    array = get_five_rot_acc(palabra, modo)
    count =0
    print len(array)
    while count < len(array):
      socket_s.send(str(len(array[count])))
      #print array[count]
      respuesta =array[count]
      count=count+1
      socket_s.send(respuesta)

HOST = '192.168.1.145' # Server IP or Hostname
PORT = 12345 # Pick an open Port (1000+ recommended), must match the client sport
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

try:
	s.bind((HOST, PORT))

except socket.error:
	print 'Bind failed'

#Gyroscope
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c


bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect
bus.write_byte_data(address, power_mgmt_1, 0)

s.listen(1)
def conexion_activa(socket_s):
	print 'Socket awaiting messages'
	(conn, addr) = s.accept()
	print 'Connected'
	return (conn, addr)


conectado_activa = 0 #Si no esta conectado, llamara a connection(s)

while True:
	if conectado_activa == 0:
		(conn, addr) = conexion_activa(s)
		conectado_activa = 1
        #print addr[0] #--> Esto es vital para la conexion por monitorizacion pasiva
	data = conn.recv(1)

	print 'I sent a message back in response to: ' + data
	reply = ''

	# process your message
	if data == '1':
		data = conn.recv(1) #Recibe el eje
		comando_rotaciones_aceleraciones(conn, data, 'r', reply)
	elif data == '2':
		data = conn.recv(1)
		comando_rotaciones_aceleraciones(conn, data, 'a', reply)
	elif data == '5':
		print 'Solicitud de monitorizcion pasiva recibida'
		reply = '1' #Como muestra de OK
		#print reply
		#conn.send(reply)
		#conn.close()
		#s.close()
		#time.sleep(6)
		#p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		while True:
		#		p.connect((addr[0],12346))
		#		time.sleep(2)
		#		print 'Esperando mas comandos'
		#		alerta = monitorizacion()
		#		if alerta == 1
					#reply = '8' #Problemas --> Especificar el tipo de problema
					#conn.send(reply)
				#elif tiempo_total = 30 min ... --> Mandar informe con todo

	#and so on and on until...
	elif data == '6':
		print 'Terminating'
		conn.send('1')
		conn.close()
		conectado_activa = 0
		#break



	# Sending reply
	#conn.send(reply)
