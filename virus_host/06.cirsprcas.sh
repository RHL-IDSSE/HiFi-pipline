source "/home/ranhl/miniconda3/etc/profile.d/conda.sh"
conda activate  cctyper_1.8.0
input=01.cp_strain_output
for file in $input/* ;do
 for name in $file/05.select_seq/* ;do
 output=$file/06.crispr
 mkdir -p $output
 file_name=$(basename $name .fasta)
 cctyper $name -t 48 $output/$file_name ;
 done
done

