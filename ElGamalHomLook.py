from petlib.ec import EcGroup
from math import ceil, sqrt
from multiprocessing import Pool
import os
import linecache

THREAD_NUMBER = 4
NUMBER_LINE_INFILE = 3999997
FILE_NAME = "table_final"
GENERATE = False

# EC setup
CURVENUMBER = 714

group = EcGroup(CURVENUMBER)
g = group.generator()
o = group.order()

# key setup
private_key = o.random()
public_key = private_key * g


def generate_lookup_table(start, end, thread_name):
    lookup_table = []
    if start == 0:
        start = 2
    curr_g = (start-1)*g
    for i in range(start, end):
        curr_g += g
        lookup_table.append(f'{str(curr_g)}:{i}')
    with open(f"table_{start}", "w") as f:
        lookup_table.sort()
        f.write(os.linesep.join(lookup_table))


def fastSearchInFile(data):
    data = str(data)
    lo = 0
    hi = NUMBER_LINE_INFILE-1
    pre_line = ""
    curr_line = "0"
    while pre_line != curr_line:
        mid = (lo + hi) // 2
        curr_line = linecache.getline(FILE_NAME, mid).split(":")
        cmp_value = curr_line[0]
        if data < cmp_value:
            hi = mid - 1
        elif data > cmp_value:
            lo = mid + 1
        else:
            return int(curr_line[1])
    return False


def bsgs_ecdlp(M):
    if str(M) == "00":
        return 0
    if M == g:
        return 1
    # Giant Step
    for i in range(m):
        temp = M - (i*m)*g
        print(temp)
        lookup_table_res = fastSearchInFile(temp)
        if lookup_table_res:
            return ((i*m + lookup_table_res) % o)
    return None


def encrypt(M):
    k = o.random()
    K = k * g
    C = (k * public_key) + (M * g)
    return (K, C)


def decrypt_bsgs(C):
    S = private_key * C[0]
    M = C[1] - S
    return bsgs_ecdlp(M)


def add(elem1, elem2):
    c11, c12 = elem1
    c21, c22 = elem2
    return (c11 + c21, c12 + c22)


# Baby Steps: Lookup Table
# m = ceil(sqrt(o))
m = 4000000
# lookup_table = {j * g: j for j in range(m)} # LOOOOL c'est beaucoup trop long
if GENERATE:
    divided_m = ceil(m/THREAD_NUMBER)
    with Pool(THREAD_NUMBER) as p:
        p.starmap(generate_lookup_table, [(i*divided_m, (i+1)*divided_m, f"process_{i}") for i in range(THREAD_NUMBER)])
else:
    # run
    print(f'decrypt(encrypt(54654)) = {decrypt_bsgs(encrypt(54654))}')
