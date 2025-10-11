import csv


input_file = "02.output.txt"

output_file = "04.vOTU_matrix.txt"


votu_to_columns = {}


with open(input_file, "r") as infile:
    reader = csv.reader(infile, delimiter="\t")
    next(reader)  
    first_column_set = set()
    for row in reader:
        first_column = row[0]  
        votu_name = row[1]  
        if votu_name not in votu_to_columns:
            votu_to_columns[votu_name] = set()
        votu_to_columns[votu_name].add(first_column)
        first_column_set.add(first_column)


first_column_list = sorted(first_column_set)
votu_names = sorted(votu_to_columns.keys())


with open(output_file, "w") as outfile:
    writer = csv.writer(outfile, delimiter="\t")
    
    writer.writerow(["vOTU_name"] + first_column_list)
    
    for votu_name in votu_names:
        row = [votu_name]
        for column in first_column_list:
            row.append("1" if column in votu_to_columns[votu_name] else "")
        writer.writerow(row)

