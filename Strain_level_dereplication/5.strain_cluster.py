import pandas as pd
import networkx as nx

def classify_genomes(input_file, output_file, ani_threshold=0.99, coverage_threshold=0.95, aai_threshold=99.5):
    
    df = pd.read_csv(input_file, sep='\t')

    
    output_lines = []

    
    for group_name, group_data in df.groupby('Group'):
        
        G = nx.Graph()

        
        for _, row in group_data.iterrows():
            if (row['ANI'] > ani_threshold) and (row['Coverage'] > coverage_threshold) and (row['AAI'] > aai_threshold):
                G.add_edge(row['Genome1'], row['Genome2'])

        
        subgroup_number = 1
        for component in nx.connected_components(G):
            for genome in component:
                output_lines.append(f"{group_name}.{subgroup_number}\t{genome}\n")
            subgroup_number += 1

        
        all_genomes = set(group_data['Genome1']).union(set(group_data['Genome2']))
        remaining_genomes = all_genomes - set(G.nodes)

        for genome in remaining_genomes:
            output_lines.append(f"{group_name}.{subgroup_number}\t{genome}\n")
            subgroup_number += 1  

    
    with open(output_file, 'w') as f:
        f.writelines(output_lines)

def main():
    input_file = '4.ani_aai_results.txt'  
    output_file = '5.grouped_genomes.txt' 

    classify_genomes(input_file, output_file)

if __name__ == '__main__':
    main()

