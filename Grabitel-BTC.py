#Copyright Slawa Ms 2024

import time
from bit import Key
from bit.format import bytes_to_wif


def load_base_balance():
    start_time = time.time()
    f = open("base_balance.txt", 'r')
    base_balance = set(f.read().split('\n'))
    stop_time = time.time()
    f.close()
    return base_balance


# -----------------------------------------------------------------------------


base_address_balance = load_base_balance()
base_address_gen = []

flag_result = False
start_time_gen = time.time()

print('     ... START ...')
key_dec =1235412369874512365412365478569321452365412369549


while 1 == 1:

    Key_compressed = Key.from_int(key_dec)
    wif_uncompressed = bytes_to_wif(Key_compressed.to_bytes(), compressed=False)
    Key_uncompressed = Key(wif_uncompressed)

    key_dec = key_dec + 1


print('END')

