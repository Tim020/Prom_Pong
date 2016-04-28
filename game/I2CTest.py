from services import I2C

i2c = I2C()

print(i2c.get_adc_value(1))
