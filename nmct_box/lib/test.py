# Example on how to read the ADXL345 accelerometer.
# Kim H. Rasmussen, 2014
import time
import spidev

# Setup SPI
spi = spidev.SpiDev()
#spi.mode = 3    <-- Important: Do not do this! Or SPI won't work as intended, or even at all.
spi.open(0,0)
spi.mode = 3

# Read the Device ID (should be xE5)
id = spi.xfer2([128,0])
print( 'Device ID (Should be 0xE5):\n'+str(hex(id[1])) + '\n')

# Read the offsets
xoffset = spi.xfer2([30 | 128,0])
yoffset = spi.xfer2([31 | 128,0])
zoffset = spi.xfer2([32 | 128,0])
print( 'Offsets: ')
print (xoffset[1])
# print yoffset[1]
# print str(zoffset[1]) + "\n\nRead the ADXL345 every half second:"

# Initialize the ADXL345
def initadxl345():
    # Enter power saving state
    spi.xfer2([45, 0])

    # Set data rate to 100 Hz
    spi.xfer2([44, 10])

    # Enable full range (10 bits resolution) and +/- 16g 4 LSB
    spi.xfer2([49, 16])

    # Enable measurement
    spi.xfer2([45, 8])

# Read the ADXL x-y-z axia
def readadxl345():
    rx = spi.xfer2([242,0,0,0,0,0,0])

    #
    out = [rx[1] | (rx[2] << 8),rx[3] | (rx[4] << 8),rx[5] | (rx[6] << 8)]
    # Format x-axis
    if (out[0] & (1<<16 - 1 )):
        out[0] = out[0] - (1<<16)
    out[0] = out[0] * 0.004 * 9.82
    # Format y-axis
    if (out[1] & (1<<16 - 1 )):
        out[1] = out[1] - (1<<16)
    out[1] = out[1] * 0.004 * 9.82
    # Format z-axis
    if (out[2] & (1<<16 - 1 )):
        out[2] = out[2] - (1<<16)
    out[2] = out[2] * 0.004 * 9.82

    return out

# Initialize the ADXL345 accelerometer
initadxl345()

# Read the ADXL345 every half second
timeout = 0.5
while(1):
    axia = readadxl345()
    # Print the reading
    print (axia[0])
    print( axia[1])
    print( str(axia[2]) + '\n')

    elapsed = time.clock()
    current = 0
    while(current < timeout):
        current = time.clock() - elapsed