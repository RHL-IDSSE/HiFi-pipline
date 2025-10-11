import os
from collections import defaultdict

def parse_ani_file(ani_file):
    ani_values = defaultdict(dict)
    with open(ani_file, 'r') as f:
        
        headers = f.readline().strip().split('\t')[0:]

        #print(f"Header length: {len(headers)}, Headers: {headers}")  

        for line in f:
            row = line.strip().split('\t')
            genome1 = row[0]  
            row_values = row[1:]  

            for i in range(len(headers)):
                genome2 = headers[i]
                ani_value = float(row_values[i])  

                
                if genome1 != genome2:
                    
                    if genome2 in ani_values[genome1]:
                        ani_values[genome1][genome2] = max(ani_values[genome1][genome2], ani_value)
                    else:
                        ani_values[genome1][genome2] = ani_value

    return ani_values

def parse_cov_file(cov_file):
    coverage_values = defaultdict(dict)
    with open(cov_file, 'r') as f:
        headers = f.readline().strip().split('\t')[0:]  
        for line in f:
            row = line.strip().split('\t')
            genome1 = row[0]
            for i in range(len(headers)):
                genome2 = headers[i]
                try:
                    coverage_value = float(row[i + 1])  
                    if genome1 != genome2:  
                        
                        if genome2 in coverage_values[genome1]:
                            coverage_values[genome1][genome2] = max(coverage_values[genome1][genome2], coverage_value)
                        else:
                            coverage_values[genome1][genome2] = coverage_value
                except ValueError:
                    print(f"Invalid coverage value at {genome1}, {genome2} in {cov_file}")
    return coverage_values

def parse_aai_file(aai_file):
    aai_values = defaultdict(dict)
    with open(aai_file, 'r') as f:
        headers = f.readline().strip().split('\t')  
        for line in f:
            row = line.strip().split('\t')
            if len(row) < 6:
                print(f"Warning: Insufficient columns in {aai_file}, skipping line: {line}")
                continue
            genome1 = row[0]
            genome2 = row[2]
            try:
                aai = float(row[5])  
                aai_values[genome1][genome2] = aai
                aai_values[genome2][genome1] = aai  
            except ValueError:
                print(f"Invalid AAI value at {genome1}, {genome2} in {aai_file}")
    return aai_values

def classify_genomes(genenome_folder, group_name, ani_aai_folder, output_txt):
    
    ani_file = f"{ani_aai_folder}/{group_name}_ANI/ANIm_percentage_identity.tab"
    cov_file = f"{ani_aai_folder}/{group_name}_ANI/ANIm_alignment_coverage.tab"
    aai_file = f"{ani_aai_folder}/{group_name}_AAI/aai/aai_summary.tsv"

    ani_values = parse_ani_file(ani_file)
    coverage_values = parse_cov_file(cov_file)
    aai_values = parse_aai_file(aai_file)

    
    with open(output_txt, 'a') as out_file:  
        for genome1 in ani_values:
            for genome2 in ani_values[genome1]:
                if genome1 != genome2:
                    ani = ani_values[genome1].get(genome2, 0)  

                    
                    coverage1 = coverage_values[genome1].get(genome2, 0)
                    coverage2 = coverage_values[genome2].get(genome1, 0)
                    coverage = max(coverage1, coverage2)  

                    aai = aai_values.get(genome1, {}).get(genome2, 0)  

                    
                    out_file.write(f"{group_name}\t{genome1}\t{genome2}\t{ani}\t{coverage}\t{aai}\n")

def main():
    genenome_folder = '2.cluster'  
    ani_aai_folder = '3.ani_aai_output'  
    output_txt = '4.ani_aai_results.txt'  

    
    with open(output_txt, 'w') as f:
        f.write("Group\tGenome1\tGenome2\tANI\tCoverage\tAAI\n")  

    
    group_folders = [folder for folder in os.listdir(genenome_folder) if folder.startswith("group")]

    for group_name in group_folders:
        print(f"Processing group: {group_name}")
        classify_genomes(genenome_folder, group_name, ani_aai_folder, output_txt)

if __name__ == '__main__':
    main()

