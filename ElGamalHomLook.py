from petlib.ec import EcGroup
import linecache

NUMBER_LINE_INFILE = 3999997
FILE_NAME = "table_final"

# EC setup
CURVENUMBER = 714

group = EcGroup(CURVENUMBER)
g = group.generator()
o = group.order()
# m = ceil(sqrt(o))
m = 4000000

# key setup
private_key = o.random()
public_key = private_key * g


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


def main():
    print(f'decrypt(encrypt(54654)) = {decrypt_bsgs(encrypt(54654))}')
    print(
        f'decrypt_bsgs(encrypt(100) + encrypt(100)) = {decrypt_bsgs(add(encrypt(100), encrypt(100)))}')


if __name__ == "__main__":
    main()
