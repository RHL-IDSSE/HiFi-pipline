source "/home/ranhl/miniconda3/etc/profile.d/conda.sh"
conda activate blast_2.15.0
input=01.cp_strain_output
db=/data2023/ranhl/DATABASE/Virus_db/SY593BBB_assemble/SY593BBB/Total
core=64
for file in $input/*;do
 inputfile=$file/03.cd_hit.fasta
 filename=$file/04.align.xls
 blastn -query $inputfile -db $db -out $filename -outfmt 6  -num_threads $core -perc_identity 95 -qcov_hsp_perc 95 -max_target_seqs 10000000 -dust no -word_size 8
done

