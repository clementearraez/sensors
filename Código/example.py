
# example-cellular-send.py - Example of using a supported modem to send messages
#                            to the Hologram Cloud.
#
# Author: Hologram <support@hologram.io>
#
# Copyright 2016 - Hologram (Konekt, Inc.)
#
# LICENSE: Distributed under the terms of the MIT License
#
import sys

sys.path.append(".")
sys.path.append("..")
sys.path.append("../..")

from Hologram.HologramCloud import HologramCloud

credentials = {'devicekey': '^hD8&#%H'}

if __name__ == "__main__":
    print ""
    print ""
    print "Testing Hologram Cloud class..."
    print ""
    print "* Note: You can obtain device keys from the Devices page"
    print "* at https://dashboard.hologram.io"
    print ""

    hologram = HologramCloud(credentials, network='cellular', authentication_type='csrpsk')#HologramCloud(dict(), network='cellular')

    print 'Cloud type: ' + str(hologram)
    startMsg = hologram.sendSMS("+34693608737", "Hello!! If you know Clemente, send him a Whatsapp! ;)")
    # enter your mobile number in the space above, area code required
    #sleep(60) # lets allow a little time for the cellular interface to restart
    print 'RESPONSE MESSAGE: ' + hologram.getResultString(startMsg)
    #recv = hologram.sendMessage('one two three!',
     #                           topics = ['TOPIC1','TOPIC2'],
      #                          timeout = 3)

    #print 'RESPONSE MESSAGE: ' + hologram.getResultString(recv)
