import spidev

def spi(adress,data = [0x00,0x00],rw = 0,bus = 0,dev = 0,max_speed = 12000000,mode = 0b00,bits_word = 8):
    spi = spidev.SpiDev()
    spi.open(bus, dev)
    spi.max_speed_hz = max_speed
    spi.lsbfirst = False
    spi.cshigh = False
    spi.mode = mode
    spi.bits_per_word = bits_word
    adress = int(convert_base(adress))
    # print(adress)
    if rw == 0:
        mask1 = 0b00000000
    elif rw == 1:
        mask1 = 0b10000000 
    mask2 = 0b00001100
    result_tx = []
    save = adress
    adress = adress >> 2
    adress = adress + mask1
    # print(adress)
    result_tx.append(adress)

    adress = save
    adress = adress << 6
    # print(adress)
    for i in range(8, 15):
        adress = adress & ~(1 << i)
    adress = adress + mask2
    # print(adress)
    result_tx.append(adress)
    result_tx.append(data[0])
    result_tx.append(data[1])
    result_rx = spi.xfer(result_tx)
    spi.close()
    return result_tx, result_rx

def convert_base(num, to_base=10, from_base=16):
    # first convert to decimal number
    if isinstance(num, str):
        n = int(num, from_base)
    else:
        n = int(num)
    # now convert decimal to 'to_base' base
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if n < to_base:
        return alphabet[n]
    else:
        return convert_base(n // to_base, to_base) + alphabet[n % to_base]

def spitest():
    txData, rxData = spi(adress = 0x00,data = [0x00,0x00])

    print(" ")
    print("TX_DATA:")
    print(txData)
    for i in range(len(rxData)):
        print (format(txData[i],'#b')) 
    print(" ")
    print("RX_DATA:")
    print(rxData)
    for i in range(len(rxData)):
        print (format(rxData[i],'#b')) 
    print(" ")
    print (format(rxData[2],'#X')+format(rxData[3],'X')) 


txData, rxData = spi(adress = 0x06C,data = [0x00,0x00],rw = 0)
print(" ")
print("TX_DATA:")
print(txData)
for i in range(len(rxData)):
    print (format(txData[i],'#b')) 
print (format(txData[0],'#X')+format(txData[1],'X'))
print(" ")
print("RX_DATA:")
print(rxData)
for i in range(len(rxData)):
    print (format(rxData[i],'#b')) 
print(" ")
print (format(rxData[3],'#X')+format(rxData[2],'X'))

# spitest()