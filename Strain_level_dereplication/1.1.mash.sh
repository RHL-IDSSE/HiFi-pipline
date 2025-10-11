#!/bin/bash
. "/home/ranhl/miniconda3/etc/profile.d/conda.sh"
conda activate mash_2.3.0

input_folder="/data2023/ranhl/SY593BBB_ABC/hm_cMAG_sMAG"
test_out=1.1.mash_output
mkdir -p $test_out
for file in $input_folder/*.fasta;do
file_name=$(basename $file .fasta)
mash sketch $file -o $test_out/$file_name;
done

