#!/bin/bash
. "/home/ranhl/miniconda3/etc/profile.d/conda.sh"
conda activate mash_2.3.0
input_folder="1.1.mash_output"
output_folder="1.2.mash_dist"


mkdir -p "$output_folder"


for reference in "$input_folder"/*.msh; do
    ref_name=$(basename "$reference" .msh)

    
    for query in "$input_folder"/*.msh; do
        query_name=$(basename "$query" .msh)

        
        if [ "$ref_name" \< "$query_name" ]; then
            
            output_prefix="$output_folder/$ref_name-vs-$query_name"

            mash dist $reference $query >> $output_folder/output.txt

        fi
    done
done

