from os import urandom
from petlib.ec import EcGroup
from math import ceil
from multiprocessing import Pool
import binascii


THREAD_NUMBER = 4
TAU = 10  # 10 bytes -> 80 bits

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
            f'{str(curr_g)[:2*TAU]}{str(i).zfill(8)}'))
    with open(f"table_{start}", "wb") as f:
        lookup_table.sort()
        f.writelines(lookup_table)


def VarTruncate(tau_start, tau_stop, file):
    curr_g = 0
    B = []
    C = [0 for _ in range(2**alpha)]

    for i in range(2**alpha):
        B.append(curr_g)
        curr_g += g
    
    for tau in range(tau_stop, tau_start, -1):
        A_tau = []
        for i, elem in enumerate(file):
            if i > (2**alpha): # not sure
                A_tau.append(elem[tau])
        for index, elem in enumerate(B):
            if C[index] == 0:
                if elem[tau] in A_tau:
                    C[index] = tau

    for tau in range(tau_stop, tau_start, -1):
        B_tau = {}
        for elem in B:
            if elem[tau] not in B_tau:
                B_tau[elem[tau]] = False
            else:
                B_tau[elem[tau]] = True

        for index, elem in enumerate(B):
            if (B_tau[elem[tau]] == True) and (C[index] < tau):
                C[index] = tau
    
    return C

def main():
    divided_m = ceil(babystep_nb/THREAD_NUMBER)
    with Pool(THREAD_NUMBER) as p:
        p.starmap(generateLookupTable, [
            (i*divided_m, (i+1)*divided_m, f"process_{i}") for i in range(THREAD_NUMBER)])


main()
