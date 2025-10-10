import os
import shutil

source_file_path = ' '  # your assembly.fasta
fasta_file_path = ' '  # your 'me_select_l&c_1.py' output file
target_folder = ' '  # your output folder

if not os.path.exists(target_folder):
    os.makedirs(target_folder)

with open(fasta_file_path, 'r') as file:
    fasta_filenames = [line.strip().lstrip('>') for line in file]

total_copied = 0

with open(source_file_path, 'r') as source_file:
    current_fasta = ''
    current_content = ''
    for line in source_file:
        if line.startswith('>'):
            if current_fasta in fasta_filenames:
                target_file = os.path.join(target_folder, f"{current_fasta}.fasta")
                with open(target_file, 'w') as output_file:
                    output_file.write(current_content)
                    total_copied += 1
            current_fasta = line.strip().lstrip('>')
            current_content = line
        else:
            current_content += line

    if current_fasta in fasta_filenames:
        target_file = os.path.join(target_folder, f"{current_fasta}.fasta")
        with open(target_file, 'w') as output_file:
            output_file.write(current_content)
            total_copied += 1

print(f"File copying completed. A total of {total_copied} files were copied.")

