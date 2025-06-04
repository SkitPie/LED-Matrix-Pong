"""Helper functions to control a chain of MAX7219 LED matrices via SPI."""

import spidev
import time
# SPI-Initialisierung
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000
NUM_MATRICES = 4
# Register-Adressen
REG_NOOP = 0x00
REG_DECODE_MODE = 0x09
REG_INTENSITY = 0x0A
REG_SCAN_LIMIT = 0x0B
REG_SHUTDOWN = 0x0C
REG_DISPLAY_TEST = 0x0F
# Display-Puffer für alle Matrizen (8x8 pro Matrix)
matrix_buffer = [[0] * 8 for _ in range(NUM_MATRICES)]
# Digit-Register für jede Zeile
REG_DIGIT = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08]
# Mapping für x-Koordinaten
mapping = {
   0: 7, 1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1, 7: 0,
   8: 7, 9: 6, 10: 5, 11: 4, 12: 3, 13: 2, 14: 1, 15: 0,
   16: 7, 17: 6, 18: 5, 19: 4, 20: 3, 21: 2, 22: 1, 23: 0,
   24: 7, 25: 6, 26: 5, 27: 4, 28: 3, 29: 2, 30: 1, 31: 0,
}
def send_data_to_all(register, value):
   """Sende einen Befehl an alle Matrizen."""
   data = [register, value] * NUM_MATRICES
   spi.xfer2(data)
def send_data(panel, row, data_value):
   """Sende Daten an ein bestimmtes Panel und eine bestimmte Zeile."""
   data = [0x00] * (NUM_MATRICES * 2)
   data[(panel * 2)] = REG_DIGIT[row]
   data[(panel * 2) + 1] = data_value
   spi.xfer2(data)
def init_display():
   """Initialisiert das Display und setzt es in den Betriebsmodus."""
   send_data_to_all(REG_SHUTDOWN, 0x01)
   send_data_to_all(REG_SCAN_LIMIT, 0x07)
   send_data_to_all(REG_DECODE_MODE, 0x00)
   send_data_to_all(REG_INTENSITY, 0x08)
   send_data_to_all(REG_DISPLAY_TEST, 0x00)
   clear_display()
def clear_display():
   """Löscht den Display-Puffer."""
   global matrix_buffer
   matrix_buffer = [[0] * 8 for _ in range(NUM_MATRICES)]
def update_display():
   """Aktualisiert das gesamte Display mit dem aktuellen Puffer."""
   for row in range(8):
       send_row(row)
def send_row(row):
   """Sendet eine komplette Zeile an alle Matrizen."""
   data = []
   for panel in range(NUM_MATRICES):
       data.append(REG_DIGIT[row])
       data.append(matrix_buffer[panel][row])
   spi.xfer2(data)
def set_pixel(x, y, state):
   """
   Setzt oder löscht ein Pixel im Puffer.
   :param x: x-Koordinate (über alle Matrizen hinweg)
   :param y: y-Koordinate (Zeile, 0-7)
   :param state: True = Pixel einschalten, False = Pixel ausschalten
   """
   global matrix_buffer
   if not (0 <= x < 32 and 0 <= y < 8):
       return
   panel = x // 8
   mapped_x = mapping.get(x, x)
   column = mapped_x % 8
   if state:
       matrix_buffer[panel][y] |= (1 << column)
   else:
       matrix_buffer[panel][y] &= ~(1 << column)
