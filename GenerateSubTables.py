from math import ceil
from multiprocessing import Pool
from petlib.ec import EcGroup
import binascii
import os


THREAD_NUMBER = 4
TAU = 33  # 10 bytes -> 80 bits
INDEX_SIZE = 4

# EC setup
CURVENUMBER = 714

group = EcGroup(CURVENUMBER)
g = group.generator()
o = group.order()
n = 16  # bits wanted ( here assuming values dont exceed 32bits )
alpha = n // 2
beta = n - alpha
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
    curr_g = g
    B = []
    C = [0 for _ in range(2**alpha)]

    for i in range(2**alpha):
        B.append(curr_g)
        curr_g += g

    for tau in range(tau_stop, tau_start, -1):
        for index_file in range(2**alpha, 2**n, 2**alpha):
            A_tau = []
            for i in range(index_file, 2**alpha+index_file):
                file.seek((INDEX_SIZE+TAU)*i)
                A_tau.append(file.read(TAU)[TAU-tau:])
            for index, elem in enumerate(B):
                if C[index] == 0:
                    if binascii.unhexlify(str(elem)[:2*TAU])[:tau] in A_tau:
                        C[index] = tau

    for tau in range(tau_stop, tau_start, -1):
        B_tau = {}
        for elem in B:
            if elem not in B_tau:
                B_tau[elem] = False
            else:
                B_tau[elem] = True

        for index, elem in enumerate(B):
            if B_tau[elem] and (C[index] < tau):
                C[index] = tau

    return C


def CreateLookupTable(tau_start, tau_stop, file):
    f = open(file, "rb")
    C = VarTruncate(tau_start, tau_stop, f)
    file_dic = {}
    for i in range(tau_start, tau_stop):
        file_dic[i] = open(f'tau_{i}', 'ab')

    for index, elem in enumerate(C):
        f.seek((INDEX_SIZE+TAU)*index)
        file_dic[elem].write(f.read(TAU)[TAU-elem:])
        file_dic[elem].write(f.read(INDEX_SIZE))

    for f_dic in file_dic.values():
        f_dic.close()

    for file in os.listdir("."):
        if file.startswith("tau_"):
            if os.stat(file).st_size == 0:
                os.remove(file)


def main():
    divided_m = ceil(2**n/THREAD_NUMBER)
    with Pool(THREAD_NUMBER) as p:
        p.starmap(generateLookupTable, [
            (i*divided_m, (i+1)*divided_m, f"process_{i}") for i in range(THREAD_NUMBER)])
    # CreateLookupTable(0, 15, "table_final")


main()
