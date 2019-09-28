from Hologram.HologramCloud import HologramCloud

import random
import string
from time import sleep
def randomString(stringLength):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

credentials = {'devicekey': '^hD8&#%H'} # replace with your unique Sim device key
cloud = HologramCloud(credentials, network='cellular', authentication_type='csrpsk')

clave = randomString(5)
mensaje_instruccion = "Bienvenido al programa de seguridad. Para activar el programa, envie primero la clave aleatoria. Su clave es: " + str(clave)
print mensaje_instruccion
recv = cloud.sendSMS("+14439044822", mensaje_instruccion)



while True: 
  sms_obj = cloud.popReceivedSMS()
  if sms_obj ==None:
    print 'U'
  else:
    if sms_obj.message == clave:
      print "Great!"
      recv = cloud.sendSMS("+14439044822", "Sistema de seguridad: ACTIVADO\n Para desactivar el programa, envie D. Para activar el programa, envie A.")
      break
    else:
      print "Fail"
      recv = cloud.sendSMS("+14439044822", "Clave Incorrecta")
  sleep(2)



