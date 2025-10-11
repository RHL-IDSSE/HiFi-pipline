import os


input_folder = "/data2023/ranhl/SY593BBB_zCrisprCas/each_phylum/10.search_virus"  
output_file = "02.output.txt"


results = []


for file_name in sorted(os.listdir(input_folder)):
    if file_name.endswith(".xls"):  
        file_path = os.path.join(input_folder, file_name)

        
        try:
            with open(file_path, "r") as f:
                second_column = set()  
                for line in f:
                    if line.strip():  
                        columns = line.strip().split("\t")
                        if len(columns) > 1:  
                            second_column.add(columns[1])  
                
                for value in sorted(second_column):  
                    results.append([file_name, value])
        except Exception as e:
            print(f"Error reading {file_name}: {e}")


with open(output_file, "w") as out_file:
    out_file.write("FileName\tSecondColumnContent\n")
    for row in results:
        out_file.write("\t".join(map(str, row)) + "\n")

print(f"Output written to {output_file}")

