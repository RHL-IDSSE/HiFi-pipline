import os
from Bio import SeqIO

def extract_sequences_by_name(input_fasta, output_folder, target_suffix):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    count = 0

    for record in SeqIO.parse(input_fasta, "fasta"):
        if record.id.endswith(target_suffix):
            output_file = os.path.join(output_folder, f"{record.id}.fasta")
            SeqIO.write([record], output_file, "fasta")
            count += 1
            print(f"Sequence {record.id} written to {output_file}")

    print(f"\nTotal {count} sequences with '{target_suffix}' suffix were selected.")

input_fasta_path = ' ' # your metaMDBG assembly.fasta
output_folder_path = ' ' # your output folder path
target_suffix = ' ' # 'c' denotes selection of circular contigs, 'l' denotes selection of linear contigs 

extract_sequences_by_name(input_fasta_path, output_folder_path, target_suffix)
