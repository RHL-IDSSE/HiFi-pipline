import os
import shutil
from collections import defaultdict

def parse_mash_result(mash_file, threshold=0.05):
    distance_dict = defaultdict(dict)
    with open(mash_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 3:
                genome1 = os.path.basename(parts[0])
                genome2 = os.path.basename(parts[1])
                distance = float(parts[2])
                if distance < threshold:
                    distance_dict[genome1][genome2] = distance
                    distance_dict[genome2][genome1] = distance
    return distance_dict

def cluster_genomes(distance_dict):
    clusters = []
    visited = set()

    for genome in distance_dict:
        if genome not in visited:
            stack = [genome]
            cluster = set()
            while stack:
                g = stack.pop()
                if g not in visited:
                    visited.add(g)
                    cluster.add(g)
                    for neighbor in distance_dict[g]:
                        if neighbor not in visited:
                            stack.append(neighbor)
            clusters.append(cluster)
    return clusters

def copy_files_to_groups(fasta_folder, clusters, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for idx, cluster in enumerate(clusters, start=1):
        group_folder = os.path.join(output_folder, f'group_{idx}')
        os.makedirs(group_folder, exist_ok=True)
        for genome in cluster:
            fasta_path = os.path.join(fasta_folder, genome)
            if os.path.isfile(fasta_path):
                shutil.copy(fasta_path, group_folder)

def copy_unclassified_genomes(fasta_folder, clusters, output_folder):
    
    classified_genomes = set()
    for cluster in clusters:
        classified_genomes.update(cluster)

    
    final_group_folder = os.path.join(output_folder, 'groupfinal')
    os.makedirs(final_group_folder, exist_ok=True)

    
    for fasta_file in os.listdir(fasta_folder):
        if fasta_file not in classified_genomes:
            fasta_path = os.path.join(fasta_folder, fasta_file)
            if os.path.isfile(fasta_path):
                shutil.copy(fasta_path, final_group_folder)

def main():
    fasta_folder = '/data2023/ranhl/SY593BBB_ABC/hm_cMAG_sMAG'  
    mash_file = '1.2.mash_dist/output.txt'  
    output_folder = '2.cluster'  

    
    distance_dict = parse_mash_result(mash_file, threshold=0.05)

    
    clusters = cluster_genomes(distance_dict)

    
    copy_files_to_groups(fasta_folder, clusters, output_folder)

    
    copy_unclassified_genomes(fasta_folder, clusters, output_folder)

if __name__ == '__main__':
    main()


