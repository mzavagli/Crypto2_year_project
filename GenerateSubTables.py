from petlib.ec import EcGroup
import os
from math import ceil, sqrt
from multiprocessing import Pool
import binascii


THREAD_NUMBER = 4

# EC setup
CURVENUMBER = 714

group = EcGroup(CURVENUMBER)
g = group.generator()
o = group.order()
n = 32  # bits wanted ( here assuming values dont exceed 32bits )
alpha = n // 2
babystep_nb = 2**alpha


def generateLookupTable(start, end, thread_name):
    lookup_table = []
    if start == 0:
        start = 2
    curr_g = (start-1)*g
    for i in range(start, end):
        curr_g += g
        lookup_table.append(binascii.unhexlify(
            f'{str(curr_g)}{str(i).zfill(8)}'))
    with open(f"table_{start}", "wb") as f:
        lookup_table.sort()
        f.writelines(lookup_table)


def generateTruncTable():
    return True


def main():
    divided_m = ceil(babystep_nb/THREAD_NUMBER)
    with Pool(THREAD_NUMBER) as p:
        p.starmap(generateLookupTable, [
            (i*divided_m, (i+1)*divided_m, f"process_{i}") for i in range(THREAD_NUMBER)])


main()
