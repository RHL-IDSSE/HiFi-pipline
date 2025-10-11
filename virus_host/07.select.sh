input=01.cp_strain_output
for folder in $input/* ;do
 output=$folder/07.spacers.fasta
 for file in $folder/06.crispr/*/spacers/*.fa;do
  cat $file >> $output
 done
done

