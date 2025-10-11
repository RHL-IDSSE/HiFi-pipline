import os
import sys

def extract_direct_repeats(input_dir):
    
    for folder in os.listdir(input_dir):
        folder_path = os.path.join(input_dir, folder)
        if os.path.isdir(folder_path):
            
            folder_name = os.path.basename(folder_path)
            
            
            output_fasta = os.path.join(folder_path, f"02.repeats.fasta")
            
            
            with open(output_fasta, 'w') as out_f:
                seq_count = 1
                
                
                for file_name in os.listdir(folder_path):
                    if file_name.endswith(".gff"):
                        gff_file = os.path.join(folder_path, file_name)
                        print(f"Processing {gff_file}...")
                        
                        with open(gff_file, 'r') as gff:
                            for line in gff:
                                
                                columns = line.strip().split('\t')
                                if len(columns) > 8 and columns[2] == "direct_repeat":
                                    
                                    attributes = columns[8]
                                    note_field = next((field for field in attributes.split(';') if field.startswith("Note=")), None)
                                    if note_field:
                                        seq = note_field.split('=')[1]
                                        
                                        out_f.write(f">{folder_name}_{seq_count}\n{seq}\n")
                                        seq_count += 1
            
            
            if seq_count == 1:
                print(f"No direct_repeat found in {folder_path}, output file is empty.")

if __name__ == "__main__":
    
    input_dir = "01.cp_strain_output"  
    extract_direct_repeats(input_dir)

