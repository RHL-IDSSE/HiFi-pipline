# HiFi-pipline
This project is a pipeline for HiFi long-read metagenomic sequencing, aimed at identifying complete MAGs (cMAGs) and near-complete single-contig MAGs (sMAGs), as well as performing strain-level redundancy removal.
We first validated the pipeline using the public ZymoBIOMICS D6331 mock dataset, the composition of which can be accessed at https://www.zymoresearch.com/products/zymobiomics-gut-microbiome-standard. This validation successfully recovered 13 cMAGs from 21 strains, including three of the five closely related Escherichia coli strains, but failed to obtain high-quality MAGs of rare prokaryotes and highly complex microeukaryotes.
<img width="993" height="1107" alt="image" src="https://github.com/user-attachments/assets/9cfb8869-5c8b-46a0-b801-12bf01ac5e27" />
## Assembly
hifiasm_meta v.0.3.1 <br>
```shell
hifiasm_meta -o ${output} -t 40 ${fq} && awk '/^S/{print ">"$2;print $3}' *.p_ctg.gfa > ${yourfilename}.p_ctg.fa
```
metaMDBG v.0.3.0 <br>
```shell
metaMDBG asm ${output} ${fq} -t 80
```
metaFlye v.2.9.2 <br>
```shell
flye --pacbio-hifi ${fq} --meta --out-dir ${output} -t 80
```
HiCanu v.2.2 <br>
```shell
canu -p ${profile} -d ${output} genomeSize=5m -pacbio-hifi ${fq} maxInputCoverage=10000 corOutCoverage=10000 corMhapSensitivity=high corMinCoverage=0 -maxThreads=80 batMemory=1400g
```
## Identification of cMAG and sMAG
### Split circular & linear contigs
The relevant scripts in the **Split_circular&linear_contigs** folder differentiate between circular and linear contigs.
### Length, completeness, and contamination filtering
For the circular and linear contigs obtained above, we filtered those longer than 100 kb, then evaluated their completeness and contamination using CheckM2 v1.0.1. Contigs with ≥90% completeness and ≤5% contamination were selected for subsequent analyses. <br>
```shell
checkm2 predict --threads 24 --input ${fa} --output-directory ${output_folder} --force -x fasta
```
### Taxonomic annotation
We performed taxonomic annotation of the high-quality MAGs (HQ-MAGs) obtained above using GTDB-Tk v.2.4.1. <br>
```shell
gtdbtk classify_wf --genome_dir ${input_folder}  --out_dir ${output_folder} --cpus 30 --force -x fasta --skip_ani_screen
```
### Filtering based on rRNA
We used Barrnap v.0.9 to predict 5S, 16S, and 23S rRNAs, and retained only MAGs containing all three. <br>
```shell
barrnap --threads 5 ${fa} > ${output_folder}/${fa_name}.gff
```
### Filtering based on the number of tRNA types
We used tRNAscan-SE v.2.0.12 to predict tRNAs, where circular contigs containing at least 20 types of tRNAs were classified as cMAGs, and those containing at least 18 types of tRNAs were classified as sMAGs. <br>
```shell
#for archaea
tRNAscan-SE -A -o ${fa_name}.txt ${fa} --thread 12
#for bacteria
tRNAscan-SE -B -o ${fa_name}.txt ${fa} --thread 12
```
### Strain-level genome dereplication
We performed Mash clustering and applied the following criteria for strain-level genome dereplication: amino acid identity (AAI) > 99.5%, average nucleotide identity (ANI) > 99%, and alignment fraction (AF) > 95%. The related scripts are stored in the **Strain_level_dereplication** folder.
## Community-level HGT prediction
We used MetaCHIP v.1.10.13 to predict community-level HGT events at the genus level. <br>
```shell
MetaCHIP PI -p ${profile} -r pcofg -t 24 -o ${output_folder} -i ${input_folder} -x fasta -taxon $taxa
MetaCHIP BP -p ${profile} -r pcofg -t 24 -o ${output_folder}
```
## Pangenome construction
We used the Panaroo v.1.5.0 to construct a species-level pangenome for 19 strains of the same ANME-1 species. <br>
```shell
panaroo -i ${input_folder}/*.gff -o ${output_folder}  --clean-mode strict --remove-invalid-genes  -a core  -t 20
```
## Virus identification
Viral sequences were retrieved from the HiFi- and Illumina-assembled contigs using the approach from the IMG/VR v4 database.  <br>
```shell
genomad end-to-end --cleanup ${assemble_file} ${output} ${genomad_db_path} --threads 24
checkv end_to_end ${potential_virus} ${checkv_output} -t 36
makeblastdb -in ${checkv_virus} -dbtype nucl -title ${your_title}  -out ${output_folder}/${your_name}
blastn -query ${checkv_virus} -db ${makeblastdb_output} -out blastn.xls -outfmt '6 std qlen slen'  -num_threads 24 -evalue 1e-5 -max_target_seqs 20000
anicalc.py -i blastn.xls -o 04.ani
aniclust.py --fna ${checkv_virus} --ani 04.ani --out 04.cluster
cut -f 1 04.cluster > 04.virus_repersent
seqkit grep -f 04.virus_repersent ${checkv_virus} -o 05.virus_repersent.fasta
```
## Virus–host association analysis
We performed high-confidence virus–host association analysis based on CRISPR-Cas systems, with the relevant code stored in the **virus-host** folder.
```shell
cctyper ${strain} -t 20 ${output_name} --prodigal meta
```
## Virus comparison analyses
```shell
prodigal -i ${virus} -o virus.gff -a virus.faa -d virus.fna -f gff -p single -m
vcontact2_gene2genome -p virus.faa -o gene2genome_new.csv -s Prodigal-FAA
vcontact2 -r virus.faa --pcs-mode MCL --vcs-mode ClusterONE  -o vcontact2_output -t 48  --proteins-fp gene2genome_new.csv
```
