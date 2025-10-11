import csv


input_file = "02.output.txt"

output_file = "03.vOTU_phylum.txt"


votu_dict = {}


with open(input_file, "r") as infile:
    reader = csv.reader(infile, delimiter="\t")
    next(reader)  
    for row in reader:
        votu_name = row[1]  
        first_column = row[0]  
        if votu_name not in votu_dict:
            votu_dict[votu_name] = []
        votu_dict[votu_name].append(first_column)


with open(output_file, "w") as outfile:
    writer = csv.writer(outfile, delimiter="\t")
    writer.writerow(["name", "values"])  
    for votu_name, values in votu_dict.items():
        writer.writerow([votu_name, ";".join(values)]) 

