from petlib.ec import EcGroup
import os
from math import ceil, sqrt
from multiprocessing import Pool


THREAD_NUMBER = 4

# EC setup
CURVENUMBER = 714

group = EcGroup(CURVENUMBER)
g = group.generator()
o = group.order()
alpha = 16
babystep_nb = 2**alpha


def generate_lookup_table(start, end, thread_name):
    lookup_table = []
    if start == 0:
        start = 2
    curr_g = (start-1)*g
    for i in range(start, end):
        curr_g += g
        lookup_table.append(f'{str(curr_g)}:{i}')
    with open(f"table_{start}", "w") as outfile:
        lookup_table.sort()
        outfile.write(os.linesep.join(lookup_table))
        outfile.write("\n")


def main():
    divided_m = ceil(babystep_nb/THREAD_NUMBER)
    with Pool(THREAD_NUMBER) as p:
        p.starmap(generate_lookup_table, [
            (i*divided_m, (i+1)*divided_m, f"process_{i}") for i in range(THREAD_NUMBER)])


main()
