from petlib.ec import EcGroup
from math import ceil, sqrt
import linecache
import random
import binascii

NUMBER_LINE_INFILE = 100003
FILE_NAME = "table_final"

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


def fastSearchInFile(data):
    data = binascii.unhexlify(str(data))
    lo = 0
    hi = NUMBER_LINE_INFILE-1
    pre_line = ""
    curr_line = "0"
    f = open(FILE_NAME, "rb")
    while 1:
        mid = (lo + hi) // 2
        f.seek(37*mid)
        curr_line = f.read(33)
        if pre_line == curr_line:
            break
        pre_line = curr_line
        if data < curr_line:
            hi = mid - 1
        elif data > curr_line:
            lo = mid + 1
        else:
            return int(binascii.hexlify(f.read(4)))
    return False


def bsgs_ecdlp(M):
    # Giant Step
    mg = babystep_nb*g
    for i in range(giantstep_nb):
        temp = M - (i*mg)
        if str(temp) == "00":
            return (i*babystep_nb % o)
        if temp == g:
            return ((i*babystep_nb + 1) % o)
        lookup_table_res = fastSearchInFile(temp)
        if lookup_table_res:
            return ((i*babystep_nb + lookup_table_res) % o)
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
    tests = [random.getrandbits(random.randint(16, 32)) for i in range(5)]
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
