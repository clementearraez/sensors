import random
import string

def randomString(stringLength):
  """Generate a random string of fixed length """
  letters = string.ascii_lowercase
  return ''.join(random.choice(letters) for i in range(stringLength))

def envio_clave(cloud):
  clave = randomString(5)
  mensaje_instruccion = "Bienvenido al programa de seguridad. Para activar el programa, envie primero la clave aleatoria. Su clave es: " + str(clave)
  print mensaje_instruccion
  recv = cloud.sendSMS("+14439044822", mensaje_instruccion)

def activar_sistema(cloud):
  while True: 
    sms_obj = cloud.popReceivedSMS()
    if sms_obj ==None:
      print "Waiting\n"
    else:
      if sms_obj.message == clave:
        print "Great!"
        recv = cloud.sendSMS("+14439044822", "Sistema de seguridad: ACTIVADO\n Para desactivar el programa, envie D. Para activar el programa, envie A.")
        break
      else:
        print "Fail"
        recv = cloud.sendSMS("+14439044822", "Clave Incorrecta")
    sleep(4)  


def a_d_sms(cloud):
    sms_obj = cloud.popReceivedSMS()
    
    if sms_obj == None:
      #print "No SMS"
      return 'U' #Unknown --> Sigues con el valor que tenias antes
    else:
      print sms_obj.message
      print sms_obj.message.lower()
      if sms_obj.message.lower() == 'd':
        print "Sistema de seguridad desactivado"
        return 'D'
      elif sms_obj.message.lower() == 'a':
        print "Sistema de seguridad activado"
        return 'A'
      else:
        print "Comando no reconocido"
        return 'U'

