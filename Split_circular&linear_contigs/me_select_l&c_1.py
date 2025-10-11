import os

input_file_path = ' '  #your assembly_info.txt path

output_file_path = ' ' 
with open(input_file_path, 'r') as input_file:
    with open(output_file_path, 'w') as output_file:
        for line in input_file:
            line = line.strip()
            columns = line.split('\t')

            if len(columns) >= 4:
                # 查找名为 "circ." 列中包含 "Y" 的行
                if  columns[3] == ' ': # 'Y' for  circular contigs, 'N' for linear contigs
                    output_file.write(columns[0] + '\n')

