source "/home/ranhl/miniconda3/etc/profile.d/conda.sh"
conda activate cd-hit_4.8.1
input=08.group_spacers_order
output=09.rd_output
mkdir -p $output
for file in $input/* ;do
 file_name=$(basename $file .fasta)
 cd-hit -i $file -o $output/$file_name -c 1.0
done

