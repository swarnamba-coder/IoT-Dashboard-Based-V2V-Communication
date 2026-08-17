from machine import I2C
from time import sleep_ms


class I2cLcd:
    LCD_CLR = 0x01
    LCD_HOME = 0x02
    LCD_ENTRY_MODE = 0x04
    LCD_DISPLAY_CTRL = 0x08
    LCD_FUNCTION = 0x20
    LCD_SET_DDRAM = 0x80

    LCD_ENTRY_LEFT = 0x02
    LCD_ENTRY_SHIFT_DECREMENT = 0x00

    LCD_DISPLAY_ON = 0x04
    LCD_CURSOR_OFF = 0x00
    LCD_BLINK_OFF = 0x00

    LCD_2LINE = 0x08
    LCD_5X8DOTS = 0x00

    LCD_BACKLIGHT = 0x08
    LCD_NOBACKLIGHT = 0x00

    ENABLE = 0x04

    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.num_lines = num_lines
        self.num_columns = num_columns
        self.backlight = self.LCD_BACKLIGHT

        sleep_ms(20)

        self.hal_write_init_nibble(0x03)
        sleep_ms(5)

        self.hal_write_init_nibble(0x03)
        sleep_ms(1)

        self.hal_write_init_nibble(0x03)
        sleep_ms(1)

        self.hal_write_init_nibble(0x02)

        self.hal_write_command(
            self.LCD_FUNCTION |
            self.LCD_2LINE |
            self.LCD_5X8DOTS
        )

        self.hal_write_command(
            self.LCD_DISPLAY_CTRL |
            self.LCD_DISPLAY_ON |
            self.LCD_CURSOR_OFF |
            self.LCD_BLINK_OFF
        )

        self.clear()

        self.hal_write_command(
            self.LCD_ENTRY_MODE |
            self.LCD_ENTRY_LEFT |
            self.LCD_ENTRY_SHIFT_DECREMENT
        )

    def hal_write_init_nibble(self, nibble):
        self.hal_write_byte(nibble << 4)

    def hal_write_command(self, command):
        self.hal_write_byte(command)

    def hal_write_data(self, data):
        self.hal_write_byte(data, True)

    def hal_write_byte(self, value, char_mode=False):
        mode = 0x01 if char_mode else 0x00

        high = value & 0xF0
        low = (value << 4) & 0xF0

        self.hal_write_nibble(high | mode)
        self.hal_write_nibble(low | mode)

    def hal_write_nibble(self, nibble):
        self.i2c.writeto(
            self.i2c_addr,
            bytes([nibble | self.backlight])
        )

        self.i2c.writeto(
            self.i2c_addr,
            bytes([nibble | self.ENABLE | self.backlight])
        )

        sleep_ms(1)

        self.i2c.writeto(
            self.i2c_addr,
            bytes([nibble | self.backlight])
        )

    def clear(self):
        self.hal_write_command(self.LCD_CLR)
        sleep_ms(2)

    def move_to(self, col, row):
        row_offsets = [0x00, 0x40, 0x14, 0x54]

        if row >= self.num_lines:
            row = self.num_lines - 1

        self.hal_write_command(
            self.LCD_SET_DDRAM |
            (col + row_offsets[row])
        )

    def putstr(self, string):
        for char in string:
            if char == "\n":
                continue

            self.hal_write_data(ord(char))
