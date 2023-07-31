import time, sys
from pyb import UART

uart = UART(3, 9600)
uart.init(9600, bits=8, parity=None, stop=1)

while(True):
    print("Hello World!\r")
    uart.write('o')
    time.sleep_ms(1000)
    uart.write('c')
    time.sleep_ms(1000)

