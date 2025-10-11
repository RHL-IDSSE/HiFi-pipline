import os
import shutil

source_folder = '/data2023/ranhl/SY593BBB_ABC/hm_cMAG_sMAG'  
target_folder = '7.strain'  
txt_file_path = '7.selected_names.txt'  


if not os.path.exists(target_folder):
    os.makedirs(target_folder)


with open(txt_file_path, 'r') as file:
    filenames = file.read().splitlines()


for root, dirs, files in os.walk(source_folder):
    for file in files:
        file_name, file_extension = os.path.splitext(file)  
        if file_name in filenames:
            source_file = os.path.join(root, file)
            target_file_name = f"{file_name}{file_extension}"  
            target_file = os.path.join(target_folder, target_file_name)
            shutil.copy(source_file, target_file)

print("complete")

