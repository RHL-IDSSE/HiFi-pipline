input=/data2023/ranhl/SY593BBB_zCrisprCas/crisprcas_293/
output=01.cp_strain_output

mkdir -p $output 

for file in "$input"/*; do
    if [ -s "$file/spacers" ]; then 
        cp -r "$file" "$output/"
    fi
done

