
#!/usr/bin/env python
'''This is an example script that ueses the vcf_to_sfs_v2 module to create a collection of snps, 
filter it and plot 2 sfs (total and filtered for only sw mutations).
Usage: script, vcf_path, bed_path, n_all_sample, num_reads
example: python final_proj.py dummy_recoded.vcf.gz dummy.bed 8 1
output path: sfs_allsites.png, sfs_sw.png.
'''

from sys import argv
from vcf_to_sfs_v2 import Collect_SNPs, Sitefrequency, SFS

#Input by user:
vcf_path="dummy_recoded.vcf.gz"
bed_path="dummy.bed"
#input parameters specified (by argv)
script, vcf_path, bed_path, n_all_sample, num_reads = argv

#Make collection of snps:
collection = Collect_SNPs() 
#get snps into the collection.
collection.get_SNPS(vcf_path, bed_path)
#create sfs object by getting the sfs from the collection of snps.
#sfs = SFS(collection.get_SFS(n_all_sample), n_all_sample)
sfs = SFS(collection.get_SFS(n_all_sample))
#generate final plot from s object: total sfs
sfs.plot_sfs("sfs_allsites.png")


#Now make a subset of the date for only SW snps:
#filter the collection
sw = collection.get_filter("SW")
#create sfs object 
sfs_sw = SFS(sw.get_SFS(n_all_sample))
#plot sfs for sw
sfs_sw.plot_sfs("sfs_sw.png")


