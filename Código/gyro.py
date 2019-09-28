#!/usr/bin/python
import smbus #Gyroscope
import math
import time

power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect
bus.write_byte_data(address, power_mgmt_1, 0)

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
        

def rot_acc_all(mode):
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
      rot_x = round(float(get_x_rotation(speed_xout_scalated, speed_yout_scalated, speed_zout_scalated)),3)
      rot_y = round(float(get_y_rotation(speed_xout_scalated, speed_yout_scalated, speed_zout_scalated)),3)
      #rot_z = round(float(get_z_rotation(speed_xout_scalated, speed_yout_scalated, speed_zout_scalated)),3)
      return rot_x, rot_y#, rot_y, rot_z
    elif mode == 'a':
      acc_x = round(speed_xout_scalated,3)
      acc_y = round(speed_yout_scalated,3)
      #acc_z = round(speed_zout_scalated,3)
      return acc_x, acc_y




