import smbus
import struct

I2CADDRESS = 0x21
bus = smbus.SMBus(1)
bus.write_byte(I2CADDRESS, 0x20)
temp = bus.read_word_data(I2CADDRESS, 0x00)
d = 0x000F & temp
e = temp >> 8
print(0xff00 >> 8)
f = (e << 8) | d
print(bin(temp) + "\n" + bin(f))
