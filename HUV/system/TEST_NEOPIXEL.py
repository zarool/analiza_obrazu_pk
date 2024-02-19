import board
import neopixel_spi
import time


pixels = neopixel_spi.NeoPixel_SPI(board.SPI(), 120)

pixels.fill(0xff0000)
time.sleep(2)