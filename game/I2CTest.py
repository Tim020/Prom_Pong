import smbus
import struct
from services import I2C 

while True:
    I2CADDRESS = 0x21
    bus = smbus.SMBus(1)
    bus.write_byte(I2CADDRESS, 0x20)
    temp = bus.read_word_data(I2CADDRESS, 0x00)
    #print(temp)
    temp = I2C.endian_swap(temp)
    temp = I2C.mask_high(temp)
    print(temp)
