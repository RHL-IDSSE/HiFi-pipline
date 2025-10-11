import os
from Bio import SeqIO

def extract_sequences(data_file, fasta_file, output_dir):
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    
    names = set()
    with open(data_file, 'r') as f:
        for line in f:
            columns = line.strip().split()
            if len(columns) > 1:
                names.add(columns[1])  

    
    fasta_sequences = SeqIO.to_dict(SeqIO.parse(fasta_file, "fasta"))

    
    seq_num = 1

    
    for name in names:
        if name:
            output_fasta = os.path.join(output_dir, f"seq_{seq_num}.fasta")

            
            if name in fasta_sequences:
                with open(output_fasta, "w") as out_file:
                    seq_record = fasta_sequences[name]
                    SeqIO.write(seq_record, out_file, "fasta")
                print(f"Extracted sequence for {name} to {output_fasta}")
                seq_num += 1  
            else:
                print(f"Name {name} not found in FASTA file")

    print(f"Sequences extracted to {output_dir}.")

def process_folder(input_dir, fasta_file):
    
    for root, dirs, files in os.walk(input_dir):
        
        data_file = None
        for file in files:
            if file.endswith(".align.xls"):  
                data_file = os.path.join(root, file)
        if data_file:
            output_dir = os.path.join(root, "05.select_seq")
            extract_sequences(data_file, fasta_file, output_dir)

if __name__ == "__main__":
    
    input_dir = "01.cp_strain_output"  
    fasta_file = "/data2023/ranhl/DATABASE/Virus_db/SY593BBB_assemble/all_assemble.fasta"
    
    process_folder(input_dir, fasta_file)

