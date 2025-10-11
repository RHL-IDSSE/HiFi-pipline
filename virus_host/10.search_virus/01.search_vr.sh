source "/home/ranhl/miniconda3/etc/profile.d/conda.sh"
conda activate blast_2.15.0
input=/data2023/ranhl/SY593BBB_zCrisprCas/each_phylum/09.rd_output
db=/data2023/ranhl/DATABASE/Virus_db/ABC_virus/vOTU/virus
core=48
for file in $input/*;do
  file_name=$(basename $file)
  blastn -query $file -db $db -out ${file_name}.xls -outfmt 6   -num_threads $core -perc_identity 95 -qcov_hsp_perc 95 -word_size 7
done

