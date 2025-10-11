import pandas as pd
import numpy as np

def calculate_scores(checkm_file):
    
    checkm_df = pd.read_csv(checkm_file, sep='\t', header=None)

    
    checkm_df[1] = pd.to_numeric(checkm_df[1], errors='coerce')  # Completeness
    checkm_df[2] = pd.to_numeric(checkm_df[2], errors='coerce')  # Contamination
    checkm_df[6] = pd.to_numeric(checkm_df[6], errors='coerce')  # N50

    
    checkm_df['Score'] = (1 * checkm_df[1] - 5 * checkm_df[2] + 0.5 * checkm_df[6].apply(lambda x: np.log(x) if x > 0 else 0))

    return checkm_df

def extract_best_genomes(grouped_file, checkm_df, output_file):
    
    grouped_df = pd.read_csv(grouped_file, sep='\t', header=None, names=['Group', 'Genome'])

   
    output_lines = []

    
    for group, group_data in grouped_df.groupby('Group'):
        
        genomes_in_group = group_data['Genome'].tolist()

        
        filtered_checkm_df = checkm_df[checkm_df[0].isin(genomes_in_group)]

        if not filtered_checkm_df.empty:
            
            cMAG_df = filtered_checkm_df[filtered_checkm_df[0].str.contains("cMAG")]

            if not cMAG_df.empty:
                
                best_gene = cMAG_df.loc[cMAG_df['Score'].idxmax()]
            else:
                
                best_gene = filtered_checkm_df.loc[filtered_checkm_df['Score'].idxmax()]

            
            output_lines.append(f"{group}\t{best_gene[0]}\t{best_gene[1]}\t{best_gene[2]}\t{best_gene[6]}\n")

    
    with open(output_file, 'w') as f:
        f.writelines(output_lines)

def main():
    grouped_file = '5.grouped_genomes.txt'  
    checkm_file = 'quality_report.tsv'  
    output_file = '6.strain_name.txt' 

    
    checkm_df = calculate_scores(checkm_file)

    extract_best_genomes(grouped_file, checkm_df, output_file)

if __name__ == '__main__':
    main()

