import os
from pathlib import Path
from collections import defaultdict
from Bio import SeqIO

def merge_fasta_by_class(txt_file, base_folder, output_folder):
    
    os.makedirs(output_folder, exist_ok=True)

    
    classification = defaultdict(list)
    with open(txt_file, 'r') as f:
        for line in f:
            folder_name, category = line.strip().split('\t')
            classification[category].append(folder_name)

    
    for category, folders in classification.items():
        output_file = Path(output_folder) / f"{category}.fasta"
        with open(output_file, 'w') as outfile:
            for folder in folders:
                spacer_file = Path(base_folder) / folder / "07.spacers.fasta"
                if spacer_file.exists():
                    for record in SeqIO.parse(spacer_file, "fasta"):
                        SeqIO.write(record, outfile, "fasta")
                else:
                    print(f"Warning: {spacer_file} does not exist and will be skipped.")

if __name__ == "__main__":
    
    txt_file = "08.group_spacers.txt"  
    base_folder = "/data2023/ranhl/SY593BBB_zCrisprCas/each_strain/01.cp_strain_output"  
    output_folder = "08.group_spacers_order" 

    merge_fasta_by_class(txt_file, base_folder, output_folder)

