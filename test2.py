import spidev

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 12000000
spi.lsbfirst = False
spi.cshigh = False
spi.mode = 0b00
spi.bits_per_word = 8
txData = [0b00000000,0b00001100,0b00000000 ,0b00000000]
rxData = spi.xfer(txData)
print(rxData)