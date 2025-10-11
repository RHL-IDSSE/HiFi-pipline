. "/home/ranhl/miniconda3/etc/profile.d/conda.sh"
conda activate CompareM_0.1.2
input_folder=2.cluster
output=3.ani_aai_output
mkdir -p $output
for file in $input_folder/group_*;do
file_name=$(basename $file)
comparem aai_wf $file $output/${file_name}_AAI  -x fasta -c 32;
done
conda deactivate

conda activate pyani_0.2.12
for file2 in $input_folder/group_*;do
file_name2=$(basename $file2)
average_nucleotide_identity.py -i $file2 -o $output/${file_name2}_ANI -m ANIm  --workers 32;
done

