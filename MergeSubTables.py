TAU = 10
INDEX_SIZE = 4


# name of the 2 tabs to merge
def merge2files(infile_names, outfile_name):
    outfile = open(f'table_{outfile_name}', "wb")  # name of the output file
    value_1 = ""
    value_2 = ""

    with open(f'table_{infile_names[0]}', "rb") as infile1, open(f'table_{infile_names[1]}', "rb") as infile2:
        value_1 = infile1.read(TAU)
        value_2 = infile2.read(TAU)
        while (value_1 or value_2) != b'':
            if value_1 == b'':
                while value_2 != b'':
                    outfile.write(value_2)
                    outfile.write(infile2.read(INDEX_SIZE))
                    value_2 = infile2.read(TAU)
            elif value_2 == b'':
                while value_1 != b'':
                    outfile.write(value_1)
                    outfile.write(infile1.read(INDEX_SIZE))
                    value_1 = infile1.read(TAU)
            if value_1 < value_2:
                outfile.write(value_1)
                outfile.write(infile1.read(INDEX_SIZE))
                value_1 = infile1.read(TAU)
            else:
                outfile.write(value_2)
                outfile.write(infile2.read(INDEX_SIZE))
                value_2 = infile2.read(TAU)
    outfile.close()


def main():
    infile_list = [("2", "16384"), ("32768", "49152"),
                   ("merge1", "merge2")]  # file to merge
    outfile_list = ["merge1", "merge2", "final"]  # names of the outfile
    assert len(infile_list) == len(outfile_list)
    for index, couple in enumerate(infile_list):
        merge2files(couple, outfile_list[index])


if __name__ == "__main__":
    main()
