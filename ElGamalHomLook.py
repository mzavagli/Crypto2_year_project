from petlib.ec import EcGroup
from math import ceil, sqrt
import random
import binascii
import os

NUMBER_LINE_INFILE = 65534
FILE_NAME = "table_final"

TAU = 10
INDEX_SIZE = 4

# EC setup
CURVENUMBER = 714

group = EcGroup(CURVENUMBER)
g = group.generator()
o = group.order()
sqrt_o = ceil(sqrt(o))
n = 32  # bits wanted ( here assuming values dont exceed 32bits )
alpha = n // 2
beta = n - alpha
babystep_nb = 2**alpha
giantstep_nb = 2**beta


# key setup
private_key = o.random()
public_key = private_key * g


def fastSearchInFile(data, f, tau):
    data = binascii.unhexlify(str(data)[:2*tau])
    lo = 0
    hi = NUMBER_LINE_INFILE-1
    pre_line = ""
    curr_line = "0"
    # TODO check if in range
    while 1:
        mid = (lo + hi) // 2
        # print(mid)
        try:
            f.seek((tau+INDEX_SIZE)*mid)
        except OSError:
            break
        curr_line = f.read(tau)
        if pre_line == curr_line:
            break
        pre_line = curr_line
        if data < curr_line:
            hi = abs(mid - 1)
        elif data > curr_line:
            lo = abs(mid + 1)
        else:
            return int(binascii.hexlify(f.read(INDEX_SIZE)))
    return False


def decryptVarTruncate(data):
    for file in os.listdir("."):
        if file.startswith("tau_"):
            f = open(file, "rb")
            result = fastSearchInFile(data, f, int(file[4:]))
            if result:
                return result


def bsgs_ecdlp(M):
    # Giant Step
    f = open(FILE_NAME, "rb")
    mg = babystep_nb*g
    for i in range(giantstep_nb):
        temp = M - (i*mg)
        if str(temp) == "00":
            f.close()
            return (i*babystep_nb % o)
        if temp == g:
            f.close()
            return ((i*babystep_nb + 1) % o)
        lookup_table_res = fastSearchInFile(temp, f)
        if lookup_table_res:
            f.close()
            return ((i*babystep_nb + lookup_table_res) % o)
    f.close()
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


def main():
    tests = [random.getrandbits(random.randint(16, 32)) for i in range(10)]
    for test_number, test in enumerate(tests):
        res = decrypt_bsgs(encrypt(test))
        print(
            f'test: {test_number+1} - decrypt(encrypt({test})) = {res} - {"Correct" if res == test else "Wrong"}')
    rand1 = random.randint(0, len(tests)-1)
    rand2 = random.randint(0, len(tests)-1)
    res = decrypt_bsgs(add(encrypt(tests[rand1]), encrypt(tests[rand2])))
    print(
        f'decrypt_bsgs(encrypt({tests[rand1]}) + encrypt({tests[rand2]})) = {res} - {"Correct" if res == (tests[rand1] + tests[rand2]) else "Wrong"}')


if __name__ == "__main__":
    main()
