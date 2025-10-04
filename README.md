# HiFi-pipline
This project is a pipeline for HiFi long-read metagenomic sequencing, aimed at identifying complete MAGs (cMAGs) and near-complete single-contig MAGs (sMAGs), as well as performing strain-level redundancy removal.
We first validated the pipeline using the public ZymoBIOMICS D6331 mock dataset, the composition of which can be accessed at https://www.zymoresearch.com/products/zymobiomics-gut-microbiome-standard. This validation successfully recovered 13 cMAGs from 21 strains, including three of the five closely related Escherichia coli strains, but failed to obtain high-quality MAGs of rare prokaryotes and highly complex microeukaryotes.
<img width="993" height="1107" alt="image" src="https://github.com/user-attachments/assets/9cfb8869-5c8b-46a0-b801-12bf01ac5e27" />
## Assembly
`hifiasm_meta` v.0.3.1 <br>
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
