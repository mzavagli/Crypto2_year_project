from petlib.ec import EcGroup
from math import ceil, sqrt
from multiprocessing import Pool
import os

THREAD_NUMBER = 4

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
    curr_g = start*g
    if start == 0:
        lookup_table.append(f'{str(0)}:{0}')
        curr_g = g
        start += 1
    for i in range(start, end):
        curr_g += g
        lookup_table.append(f'{str(curr_g)}:{i}')
    with open(f"table_{start}", "w") as f:
        lookup_table.sort()
        f.write(os.linesep.join(lookup_table))


def bsgs_ecdlp(M):
    global divided_m
    if M == g:
        return 1
    m = ceil(sqrt(o))
    m = 4000000
    # Baby Steps: Lookup Table
    # lookup_table = {j * g: j for j in range(m)} # LOOOOL c'est beaucoup trop long
    divided_m = ceil(m/THREAD_NUMBER)
    with Pool(THREAD_NUMBER) as p:
        p.starmap(generate_lookup_table, [(i*divided_m, (i+1)*divided_m, f"process_{i}") for i in range(THREAD_NUMBER)])
    # Giant Step
    """
    for i in range(m):
        temp = M - (i*m)*g
        if temp in lookup_table:
            return (i*m + lookup_table[temp]) % o
    """
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


print(f'decrypt(encrypt(2)) = {decrypt_bsgs(encrypt(2))}')
