import spidev
from adxl_base import ADXL345_Base
import time

WRITE_MASK = 0x0
READ_MASK = 0x80
MULTIREAD_MASK = 0x40

class ADXL345(ADXL345_Base):

  def __init__(self, spi_bus=0, spi_device=0):
    self.spi = spidev.SpiDev()
    self.spi.open(spi_bus, spi_device)
    self.spi.mode = 0b11
    self.spi.max_speed_hz = 5000000
    self.spi.bits_per_word = 8
    self.spi.threewire = False
    self.spi.cshigh = False
    self.spi.lsbfirst = False

  def get_register(self, address):
    value = self.spi.xfer2( [ (address & 0x3F) | READ_MASK ] )
    return value;

  def get_registers(self, address, count):
    self.spi.writebytes( [( address & 0x3F ) | READ_MASK | MULTIREAD_MASK] )
    value = self.spi.readbytes(count)
    return value

  def set_register(self, address, value):
    self.spi.writebytes( [ address, value ] )


adxl = ADXL345()

# Print device ID
deviceId = adxl.get_device_id()
print("ADXL DeviceID: " + str(deviceId))

# Set data rate at about 8 hz
rate_hz = adxl.set_data_rate(8, 1)
print("Rate: " + str(rate_hz) + " hz")

# Select Range
adxl.set_range(16, True)

# Turn off sleep mode (default when powered)
adxl.power_on()

# Indefinitely print acceleration measures
print("Press CTRL-C to stop")
while True:
    val = adxl.get_axes()
    print("X,Y,Z: " + str(val))
    time.sleep(1)