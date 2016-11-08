'''This folder contains a module and example files to estime a SFS from a vcf file.
These information can be filtered for 
different purposes in terms of number of alleles samples, min numbe rof reads covered, class of mutation, genomic region.

input files: 
1.  vcf file. Needs to be ocmpressed and index with tabix.
2.	BED files to filter for example repetitive regions.

input parameters by user:
1. num_reads: min number of reads for each individual.
2. num_individuals: number of genotyped individuals.

output1: 
1. plots.

Example files in the example directory

usage example: 
#input parameters specified (by argv): script, vcf_path, bed_path, n_all_sample, num_reads = argv
python final_proj.py dummy_recoded.vcf.gz dummy.bed 8 1

'''
