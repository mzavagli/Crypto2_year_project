table_names = ("merged1", "merged2")  # name of the 2 tabs to merge

outfile = open("table_final", "w")  # name of the output file
pre1 = ""
pre2 = ""
line_file1 = "0"
line_file2 = "0"

with open(f'table_{table_names[0]}') as infile1, open(f'table_{table_names[1]}') as infile2:
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
