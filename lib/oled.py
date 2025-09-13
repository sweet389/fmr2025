from machine import I2C
import time

SET_CONTRAST = 0x81
SET_ENTIRE_ON = 0xA4
SET_NORM_INV = 0xA6
SET_DISP = 0xAE
SET_MEM_ADDR = 0x20
SET_COL_ADDR = 0x21
SET_PAGE_ADDR = 0x22
SET_DISP_START_LINE = 0x40
SET_SEG_REMAP = 0xA0
SET_MUX_RATIO = 0xA8
SET_COM_OUT_DIR = 0xC0
SET_DISP_OFFSET = 0xD3
SET_COM_PIN_CFG = 0xDA
SET_DISP_CLK_DIV = 0xD5
SET_PRECHARGE = 0xD9
SET_VCOM_DESEL = 0xDB
SET_CHARGE_PUMP = 0x8D

class SSD1306:
    def __init__(self, width, height, external_vcc):
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height // 8
        self.buffer = bytearray(self.width * self.pages)
        self.init_display()

    def init_display(self):
        for cmd in (
            SET_DISP | 0x00,         # display off
            SET_MEM_ADDR, 0x00,      # horizontal addressing mode
            SET_DISP_START_LINE | 0x00,
            SET_SEG_REMAP | 0x01,    # column addr 127 mapped to SEG0
            SET_MUX_RATIO, self.height - 1,
            SET_COM_OUT_DIR | 0x08,  # scan from COM[N] to COM0
            SET_DISP_OFFSET, 0x00,
            SET_COM_PIN_CFG, 0x12 if self.height == 64 else 0x02,
            SET_CONTRAST, 0x7F,
            SET_PRECHARGE, 0x22 if self.external_vcc else 0xF1,
            SET_VCOM_DESEL, 0x30,    # 0.83*Vcc
            SET_ENTIRE_ON,           # output follows RAM contents
            SET_NORM_INV,            # not inverted
            SET_CHARGE_PUMP, 0x10 if self.external_vcc else 0x14,
            SET_DISP | 0x01,         # display on
        ):
            self.write_cmd(cmd)

    def write_cmd(self, cmd):
        raise NotImplementedError

    def write_data(self, buf):
        raise NotImplementedError

    def show(self):
        raise NotImplementedError

    def fill(self, col):
        fill_byte = 0xFF if col else 0x00
        for i in range(len(self.buffer)):
            self.buffer[i] = fill_byte

    def pixel(self, x, y, col):
        if not (0 <= x < self.width and 0 <= y < self.height):
            return
        page = y // 8
        shift = y % 8
        index = x + page * self.width
        if col:
            self.buffer[index] |= (1 << shift)
        else:
            self.buffer[index] &= ~(1 << shift)

    def text(self, string, x, y):
        import framebuf
        fb = framebuf.FrameBuffer(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        fb.text(string, x, y, 1)

class SSD1306_I2C(SSD1306):
    def __init__(self, width, height, i2c, addr=0x3C, external_vcc=False):
        self.i2c = i2c
        self.addr = addr
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        self.i2c.writeto(self.addr, bytearray([0x00, cmd]))

    def write_data(self, buf):
        self.i2c.writeto(self.addr, bytearray([0x40]) + buf)

    def show(self):
        for page in range(self.pages):
            self.write_cmd(SET_PAGE_ADDR)
            self.write_cmd(page)
            self.write_cmd(self.pages - 1)
            self.write_cmd(SET_COL_ADDR)
            self.write_cmd(0)
            self.write_cmd(self.width - 1)
            start = self.width * page
            end = start + self.width
            self.write_data(self.buffer[start:end])