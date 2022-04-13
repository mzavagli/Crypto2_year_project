import time
from os.path import exists


# name of the 2 tabs to merge
def merge2files(infile_names, outfile_name):
    outfile = open(f'{outfile_name}', "wb")  # name of the output file
    value_1 = ""
    value_2 = ""
    i = 0

    with open(f'{infile_names[0]}', "rb") as infile1, open(f'{infile_names[1]}', "rb") as infile2:
        value_1 = infile1.read(33)
        value_2 = infile2.read(33)
        while (value_1 or value_2) != b'':
            if value_1 == b'':
                while value_2 != b'':
                    outfile.write(value_2)
                    outfile.write(infile2.read(4))
                    value_2 = infile2.read(33)
            elif value_2 == b'':
                while value_1 != b'':
                    outfile.write(value_1)
                    outfile.write(infile1.read(4))
                    value_1 = infile1.read(33)
            if value_1 < value_2 :
                outfile.write(value_1)
                outfile.write(infile1.read(4))
                value_1 = infile1.read(33)
            else:
                outfile.write(value_2)
                outfile.write(infile2.read(4))
                value_2 = infile2.read(33)

    outfile.close()


def main():
    infile_list = [("2", "25000"), ("50000", "75000"),
                   ("merge1", "merge2")]  # file to merge
    outfile_list = ["merge1", "merge2", "final"]  # names of the outfile
    assert len(infile_list) == len(outfile_list)
    for index, couple in enumerate(infile_list):
        merge2files(couple, outfile_list[index])


if __name__ == "__main__":
    merge2files(["table_262144", "table_524288"], "table_merge")