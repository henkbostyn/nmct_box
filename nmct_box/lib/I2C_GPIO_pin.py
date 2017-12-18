import RPi.GPIO as GPIO
import time


class I2C:


    def __init__(self,SDA,SCL, adres):
        self.SDA = SDA
        self.SCL = SCL
        self.__setup()
        self.__startAdres(adres)

    def __setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SDA, GPIO.OUT)
        GPIO.setup(self.SCL, GPIO.OUT)

    def __startAdres(self, adres):
        self.__start()
        self.sendByte(adres)

    def __start(self):
        GPIO.output(self.SDA,True)
        GPIO.output(self.SCL,GPIO.HIGH)
        time.sleep(0.01)

        GPIO.output(self.SDA,GPIO.LOW)
        time.sleep(0.01)

        GPIO.output(self.SCL,GPIO.LOW)
        time.sleep(0.01)

    def __writeBit(self, bit):
        GPIO.output(self.SDA,bit)
        GPIO.output(self.SCL,GPIO.LOW)
        GPIO.output(self.SCL,GPIO.HIGH)
        GPIO.output(self.SCL,GPIO.LOW)


    def sendByte(self, byte):
        for i in range(7,-1,-1):
            if ((byte & (1 << i)) > 0 ):
                self.__writeBit(True)
            else:
                self.__writeBit(False)
        self.__ack()

    def __ack(self):
        self.__writeBit(False)



