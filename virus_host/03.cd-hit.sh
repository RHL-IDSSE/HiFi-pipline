source "/home/ranhl/miniconda3/etc/profile.d/conda.sh"
conda activate cd-hit_4.8.1
input=01.cp_strain_output
for file in $input/*;do
 inputfile=$file/02.repeats.fasta
 cd-hit -i $inputfile  -o $file/03.cd_hit.fasta -c 1.0
done

