import os

def filter_and_save_to_folder(input_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    count = 0 

    with open(input_path, 'r') as input_file:
        current_sequence = ""
        keep_sequence = False

        for line in input_file:
            if line.startswith('>'):
                if keep_sequence:
                    count += 1
                    sequence_name = current_sequence.split()[0].replace('>', '')
                    output_path = os.path.join(output_folder, f'{sequence_name}.fasta')
                    with open(output_path, 'w') as output_file:
                        output_file.write(current_sequence)
                keep_sequence = False
                current_sequence = line
                if "suggestBubble=no" in line and "suggestCircular=no" in line: # you need change suggestCircular=no or yes
                    keep_sequence = True
            else:
                current_sequence += line

        
        if keep_sequence:
            count += 1
            sequence_name = current_sequence.split()[0].replace('>', '')
            output_path = os.path.join(output_folder, f'{sequence_name}.fasta')
            with open(output_path, 'w') as output_file:
                output_file.write(current_sequence)

    print(f"File copying completed. A total of {count} files were copied. ")


input_file_path = ' ' # your HiCanu assembly.fasta
output_folder_path = ' ' # your output folder

filter_and_save_to_folder(input_file_path, output_folder_path)
