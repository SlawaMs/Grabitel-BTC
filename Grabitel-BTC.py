# Copyright Slawa Ms 2024

import time
from bit import Key
from bit.format import bytes_to_wif

# You need to download the actual Blockchain Database Dump from e.g. https://gz.blockchair.com/bitcoin/addresses/ (>2.5 Gb).
# Unzip and rename the file to 'wallets.txt'
# wallets_file_name = 'wallets.txt'
wallets_file_name = 'wallets_short.txt'
result_file_name = ''
bingo_file_name = ''

# Setup options
block_size = 300
short_address_size = 7 # max= 34
satoshi_min_balance = 2000

short_addresses_base = []
# --------------------------------------------------------------------------------
def load_base_balance():
    f = open(wallets_file_name, 'r')
    base_balance = set(f.read().split('\n'))
    f.close()
    return base_balance

def get_start_privat_address():
    return int(0x441c03e3c0c3bfec5c23bf0beece2f24590e996531051f83cb647c5b9144b488)
    #HEX 441c03e3c0c3bfec5c23bf0beece2f24590e996531051f83cb647c5b9144b488
    #DEC 30806772266923329741855079824762291006883982884022158696581543537341635015816



# --------------------------------------------------------------------------------
print('     ... Load base ...')

start_time = time.time()
base_addresses_balance = load_base_balance()
legacy_count = 0
for addr in base_addresses_balance:
    if addr[0] == '1': #Legacy Bitcoin addresses start 1
        legacy_count += 1
        try:
            satoshi = int(addr.split()[-1])
            if satoshi >= satoshi_min_balance:
                short_addresses_base.append(addr[0:short_address_size])
        except: pass
stop_time = time.time()


print('Database loaded in :  ', stop_time - start_time, "seconds")
print('Total addresses in the database:   ', len(base_addresses_balance))
print('Legacy addresses in the database:  ', legacy_count)
print('Addresses with the balance:  ', len(short_addresses_base))
print('---------------------------------------')
base_address_balance = []


print('     ... END   ...')

# ================================================================================
start_address_dec = get_start_privat_address()

block_number = 0
start_time = time.time()
while 1 == 1: # To stop the program, press 'Ctrl+ C'
    block_number += 1
    start_block_time = time.time()
    for i in range(block_size):
        key_compressed = Key.from_int(start_address_dec + i)
        wif_uncompressed = bytes_to_wif(key_compressed.to_bytes(), compressed= False)
        key_uncompressed = Key(wif_uncompressed).address
        short_key = key_uncompressed[0:short_address_size]
        if short_key in short_addresses_base:
            print('Found it! ', short_key, key_uncompressed)
    block_time = time.time() - start_block_time
    total_time = (time.time() - start_time)
    print('Block processing time:  #'+ str(block_number) + '     ' + time.strftime('%X', time.gmtime(block_time)))  #'%H:%M:%S'172900
    print('Total operating time:  ' + f'{(total_time // 86400):g}' + ' days and ' + time.strftime('%X', time.gmtime(total_time)))  # '%H:%M:%S'172900

# ================================================================================