from random import randint
import time
import threading

from lib.neopixel import Adafruit_NeoPixel

class NmctPixel:


    #LEDS        = 24     # Aantel LEDS
    PIN         = 12   # GPIO 18 / PIN 12
    BRIGHTNESS  = 255    # min 0 / max 255

    KLEUR_R     = randint(0,255)
    KLEUR_G     = randint(0,255)
    KLEUR_B     = randint(0,255)

    def __init__(self,numPixels):
        self.LEDS = numPixels
        self.ring = Adafruit_NeoPixel(self.LEDS,NmctPixel.PIN, 800000, 5, False,NmctPixel.BRIGHTNESS)
        #
        self.ring.begin()

    def loopLed(self, color, wait_ms):
        for i in range(self.LEDS):
            self.ring.setPixelColor(i,color)
            self.ring.show()
        # for i in range(self.LEDS):
        #     self.ring.setPixelColor(i, color)
        #     self.ring.show()
        #     time.sleep(wait_ms / 1000.0)
        #     self.ring.setPixelColor(i, 0)
        #     self.ring.setPixelColor(i - 1, 0)
        #
        # for i in range(self.LEDS - 1, -1, -1):
        #     self.ring.setPixelColor(i, color)
        #     self.ring.show()
        #     time.sleep(wait_ms / 1000.0)
        #     self.ring.setPixelColor(i, 0)
            self.ring.setPixelColor(i + 1, 0)

    def theaterChase(self, color, wait_ms=50, iterations=10):
        """Movie theater light style chaser animation."""
        for j in range(iterations):
            for q in range(3):
                for i in range(0, self.LEDS, 3):
                    self.ring.setPixelColor(i + q, color)
                self.ring.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.LEDS, 3):
                    self.ring.setPixelColor(i + q, 0)

    def wheel(self,pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return NmctPixel.Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return NmctPixel.Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return NmctPixel.Color(0, pos * 3, 255 - pos * 3)

    def rainbowCycle(self, wait_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""

        for j in range(256 * iterations):
            for i in range(self.ring.numPixels()):
                self.ring.setPixelColor(i, self.wheel((int(i * 256 / self.ring.numPixels()) + j) & 255))
                self.ring.show()
            time.sleep(wait_ms / 1000.0)

    def theaterChaseRainbow(self, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
            for q in range(3):
                for i in range(0, self.ring.numPixels(), 3):
                    self.ring.setPixelColor(i + q, self.wheel((i + j) % 255))
                    self.ring.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.ring.numPixels(), 3):
                    self.ring.setPixelColor(i + q, 0)

    def resetLeds(self, color, wait_ms=10):
        for i in range(self.ring.numPixels()):
            self.ring.setPixelColor(i, color)
            self.ring.show()

    @staticmethod
    def Color(red, green, blue, white = 0):
        """Convert the provided red, green, blue color to a 24-bit color value.
        Each color component should be a value 0-255 where 0 is the lowest intensity
        and 255 is the highest intensity.
        """
        return (white << 24) | (red << 16)| (green << 8) | blue

    @staticmethod
    def call_method(method_name):
        threading._start_new_thread(NmctPixel.__start_thread,('show_pixel',1,method_name))


    @staticmethod
    def __start_thread(threadname,delay,method_name):
        print('show neopixel')
        print(method_name)
        ring = NmctPixel(24)
        if method_name== 'loopLed':
             ring.loopLed(NmctPixel.Color(255, 255,255), 100)
        if method_name == 'theaterChase':
            ring.theaterChase(NmctPixel.Color(255,255, 255))
            ring.theaterChase(NmctPixel.Color(0,0, 0))
            ring.theaterChase(NmctPixel.Color(0, 0, 255))
        if method_name == 'rainbowCycle':
            ring.rainbowCycle(10,2)

        if method_name == 'theaterChaseRainbow':
            ring.theaterChaseRainbow(10)
        if method_name == 'resetLeds':
            ring.resetLeds(NmctPixel.Color(0, 0, 0),1)



