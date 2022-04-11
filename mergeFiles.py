import time
from os.path import exists


# name of the 2 tabs to merge
def merge2files(infile_names, outfile_name):
    outfile = open(f'table_{outfile_name}', "w")  # name of the output file
    pre1 = ""
    pre2 = ""
    line_file1 = "0"
    line_file2 = "0"

    while (not exists(f'table_{infile_names[0]}')) or (not exists(f'table_{infile_names[1]}')):
        time.sleep(2)

    with open(f'table_{infile_names[0]}') as infile1, open(f'table_{infile_names[1]}') as infile2:
        while 1:
            if pre1 != line_file1:
                line_file1 = infile1.readline()
                pre1 = line_file1
            if pre2 != line_file2:
                line_file2 = infile2.readline()
                pre2 = line_file2
            if not line_file1:
                if not line_file2:
                    break
                else:
                    for line in infile2.readlines():
                        outfile.write(f'{line}\n')
                    break
            if not line_file2:
                for line in infile1.readlines():
                    outfile.write(f'{line}\n')
                break
            if line_file1 < line_file2:
                outfile.write(line_file1)
                line_file1 = ""
            else:
                outfile.write(line_file2)
                line_file2 = ""

    outfile.close()


def main():
    infile_list = [("2", "1000000"), ("2000000", "3000000"),
                   ("merge1", "merge2")]  # file to merge
    outfile_list = ["merge1", "merge2", "final"]  # names of the outfile
    assert len(infile_list) == len(outfile_list)
    for index, couple in enumerate(infile_list):
        merge2files(couple, outfile_list[index])


if __name__ == "__main__":
    main()
