import spidev
import logging
import time
import sys

def blink():
    for i in range(0,10):
        spi2(adress = 0x06C,data = [0x00,0x40],rw = 1,max_speed = 5000000)
        spi2(adress = 0x084,data = [0x00,0x00],rw = 1,max_speed = 5000000)
        time.sleep(1)
        spi2(adress = 0x06C,data = [0x00,0x00],rw = 1,max_speed = 5000000)
        spi2(adress = 0x084,data = [0x00,0x40],rw = 1,max_speed = 5000000)
        time.sleep(1)
    spi2(adress = 0x084,data = [0x00,0x00],rw = 1,max_speed = 5000000)
    spi2(adress = 0x06C,data = [0x00,0x00],rw = 1,max_speed = 5000000)
    
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
    for i in range(0,len(data)):
        result_tx.append(data[i])
    result_rx = spi.xfer(result_tx)
    spi.close()
    return result_tx, result_rx

def spi2(adress,data = [0x00,0x00],rw = 0,bus = 0,dev = 0,max_speed = 12000000,mode = 0b00,bits_word = 8):
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
    adress = adress >> 4
    adress = adress + mask1
    # print(adress)
    result_tx.append(adress)

    adress = save
    adress = adress << 4
    # print(adress)
    for i in range(8, 15):
        adress = adress & ~(1 << i)
    adress = adress + mask2
    # print(adress)
    result_tx.append(adress)
    for i in range(0,len(data)):
        result_tx.append(data[i])
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
    print (format(rxData[3],'#X')+format(rxData[2],'X')) 

def iterate_over_values(start = 0x00, stop = 0x02):
    adress = start
    while(adress < stop):
        print(hex(adress))
        logging.info(" ")
        logging.info(hex(adress))
        txData, rxData = spi2(adress = adress,data = [0x00,0x00],rw = 0)
        TX = format(txData[0],'#X')+format(txData[1],'X')
        RX = format(rxData[3],'#X')+format(rxData[2],'X')
        logging.info("TX:" + TX)
        logging.info("RX:" + RX)
        logging.info(" ")
        adress = adress + 2
    print("\033[32m {}".format("Done"))
    print("\033[37m {}".format(" "))

# logging.basicConfig(level=logging.DEBUG, filename=r'log.log', filemode='w',
#                         format='%(name)s - %(levelname)s - %(message)s')

# iterate_over_values(stop = 0x01C)
def port_1_power_off():
    spi2(adress = 0x04C,data = [0x20,0x39],rw = 1,max_speed = 5000000)

def port_1_power_on():
    spi2(adress = 0x04C,data = [0x20,0x31],rw = 1,max_speed = 5000000)

def port_2_power_off():
    spi2(adress = 0x058,data = [0x20,0x39],rw = 1,max_speed = 5000000)

def port_2_power_on():
    spi2(adress = 0x058,data = [0x20,0x31],rw = 1,max_speed = 5000000)

def select_fiber_mode():
    spi2(adress = 0x0D8,data = [0xFC,0x00],rw = 1,max_speed = 5000000)
def select_coper_mode():
    spi2(adress = 0x0D8,data = [0x3C,0x00],rw = 1,max_speed = 5000000)

method_name = sys.argv[1]
try: 
    parameter_name = sys.argv[2]
    getattr(sys.modules[__name__], method_name)(parameter_name)
    print(method_name)
    print(parameter_name)
except:
    print("There is no parameter")
    getattr(sys.modules[__name__], method_name)()
    print(method_name)


# txData, rxData = spi2(adress = 0x04C,data = [0x20,0x31],rw = 1,max_speed = 5000000)
# logging.info(" ")
# logging.info(txData)
# logging.info(rxData)
# logging.info(" ")
# print(" ")
# print("TX_DATA:")
# print(txData)
# for i in range(len(rxData)):
#     print (format(txData[i],'#b')) 
# print (format(txData[0],'#X')+format(txData[1],'X'))
# print(" ")
# print("RX_DATA:")
# print(rxData)
# for i in range(len(rxData)):
#     print (format(rxData[i],'#b')) 
# print(" ")
# print (format(rxData[3],'#X')+format(rxData[2],'X'))
# blink()

# spitest()
# port_2_power_on()