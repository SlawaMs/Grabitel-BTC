# Copyright Slawa Ms 2024

import time
from bit import Key
from bit.format import bytes_to_wif
import secrets


# You need to download the actual Blockchain Database Dump from e.g. https://gz.blockchair.com/bitcoin/addresses/ (>2.5 Gb).
# Unzip and rename the file to 'wallets.txt'
wallets_file_name = 'wallets.txt'
# wallets_file_name = 'wallets_short.txt'
result_file_name = ''
bingo_file_name = 'bingo.txt'

# Setup options
block_size = 20000
short_address_size = 10     # max= 34
satoshi_min_balance = 2000  # min= 1

short_addresses_base = []
# --------------------------------------------------------------------------------
def load_base_balance():
    f = open(wallets_file_name, 'r')
    base_balance = set(f.read().split('\n'))
    f.close()
    return base_balance

def get_start_privat_address():
    maxDec = 115792089237316195423570985008687907852837564279074904382605163141518161494337
    spa = int(secrets.token_hex(32), 16)
    if spa + block_size > maxDec:
        return maxDec - block_size
    else:
        return spa
    #maxDec 115792089237316195423570985008687907852837564279074904382605163141518161494337
    #maxHEX FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
# --------------------------------------------------------------------------------
print('     ... Load base ...')

start_time = time.time()
base_addresses_balance = load_base_balance()
legacy_count = 0
for addr in base_addresses_balance:
    if addr[0] == '1': #Legacy Bitcoin addresses starts with 1
        legacy_count += 1
        try:
            satoshi = int(addr.split()[-1])
            if satoshi >= satoshi_min_balance:
                short_addresses_base.append(addr[0:short_address_size])
        except: pass
short_addresses_base = set(short_addresses_base)
stop_time = time.time()


print('Database loaded in :  ', stop_time - start_time, "seconds")
print('Total addresses in the database:   ', len(base_addresses_balance))
print('Legacy addresses in the database:  ', legacy_count)
print('Addresses with the balance:  ', len(short_addresses_base))
print('---------------------------------------')
base_address_balance = []


print('     ... END   ...')
print('Start ...')
# ================================================================================


block_number = 0
start_time = time.time()
while True: # To stop the program, press 'Ctrl+ C'
    start_address_dec = get_start_privat_address()
    block_number += 1
    # start_block_time = time.time()
    for i in range(block_size):
        key_compressed = Key.from_int(start_address_dec + i)
        wif_uncompressed = bytes_to_wif(key_compressed.to_bytes(), compressed= False)
        key_uncompressed = Key(wif_uncompressed).address
        short_key = key_uncompressed[0:short_address_size]
        if short_key in short_addresses_base:
            print('Found it! ', short_key, key_uncompressed)
            adress_text = ('{0:,}'.format(block_number * block_size).replace(',', '.') + ' wallets addresses was checked out.' + '\n' +
                           'Privat key Hex = ' + str(hex(start_address_dec + i))[2:] + '\n' +
                           'Privat key WIF = ' + str(wif_uncompressed) + '\n' +
                           'Uncompressed address legacy (P2PKH) = ' + str(key_uncompressed) + '\n' +
                           '=====================================' + '\n')
            try:
                f = open(bingo_file_name, "a")
                f.write(adress_text)
                f.close()
            except: pass

    # block_time = time.time() - start_block_time
    total_time = (time.time() - start_time)
    if (block_number * block_size) % 1000000 == 0:
        # print('Block processing time:  #'+ str(block_number) + '     ' + time.strftime('%X', time.gmtime(block_time)))
        print('{0:,}'.format(block_number * block_size).replace(',', '.') + ' wallets addresses was checked out.')
        print('Total operating time:  ' + f'{(total_time // 86400):g}' + ' days and ' + time.strftime('%X', time.gmtime(total_time)))
        print('')
# ================================================================================