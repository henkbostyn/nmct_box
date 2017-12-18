from lib.I2C_GPIO_pin import I2C
import time


class GPIOLCD:
    # display werkt goed zonder levelshifter maar moet een voeding krijgen van 5 Volt.
    I2C_ADDR = 0x7e  # I2C device address  0x3f   #adres in de pi dus nog 1 naar links shiften
    LCD_WIDTH = 16  # Maximum characters per line

    # Define some device constants
    LCD_CHR = 1  # Mode - Sending data
    LCD_CMD = 0  # Mode - Sending command

    LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
    LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line
    LCD_SCROLL = 0x18
    LCD_CURSOR_MOVE = 0x10

    # Timing constants
    E_PULSE = 0.005
    E_DELAY = 0.001

    ENABLE =0x4

    LCD_BACKLIGHT = 0x08  # On

    # LCD_BACKLIGHT = 0x00  # Off

    def __init__(self, SDA, SCL):
        self.GPIO_I2C = I2C(SDA, SCL, GPIOLCD.I2C_ADDR)
        self.__lcd_init()

    def __lcd_init(self):
        # Initialise display
        self.__lcd_byte(0x33, GPIOLCD.LCD_CMD)  # 110011 Initialise
        self.__lcd_byte(0x32, GPIOLCD.LCD_CMD)  # 110010 Initialise
        self.__lcd_byte(0x28, GPIOLCD.LCD_CMD)  # 101000 Data length, number of lines, font size
        self.__lcd_byte(0x0C, GPIOLCD.LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
        self.__lcd_byte(0x01, GPIOLCD.LCD_CMD)  # 000001 Clear display
        time.sleep(GPIOLCD.E_DELAY)

    def __lcd_byte(self, bits, mode):
        # Send byte to data pins
        # bits = the data
        # mode = 1 for data
        #        0 for command
        bits_high = mode | (bits & 0xF0) | GPIOLCD.LCD_BACKLIGHT
        bits_low =  mode | ((bits<<4) & 0xF0) | GPIOLCD.LCD_BACKLIGHT
        # High bits
        self.GPIO_I2C.sendByte(bits_high)
        self.__lcd_toggle_enable(bits_high)

        # Low bits
        self.GPIO_I2C.sendByte(bits_low)
        self.__lcd_toggle_enable(bits_low)

    def __lcd_toggle_enable(self, bits):
        # Toggle enable
        time.sleep(GPIOLCD.E_DELAY)
        self.GPIO_I2C.sendByte( bits | GPIOLCD.ENABLE)
        time.sleep(GPIOLCD.E_PULSE)
        self.GPIO_I2C.sendByte( bits & ~GPIOLCD.ENABLE)
        time.sleep(GPIOLCD.E_DELAY)


    def lcd_write_text(self,message):
        for i in range(len(message)):
            self.__lcd_byte(ord(message[i]), GPIOLCD.LCD_CHR)
            if i == 15:
                self.__lcd_byte(GPIOLCD.LCD_LINE_2, GPIOLCD.LCD_CMD)
            if i == 31:
                self.__lcd_byte(GPIOLCD.LCD_SCROLL,GPIOLCD.LCD_CMD)



    def lcd_write_line(self,message,line):
        self.__lcd_byte(line, GPIOLCD.LCD_CMD)
        for i in range(len(message)):
            self.__lcd_byte(ord(message[i]), GPIOLCD.LCD_CHR)



