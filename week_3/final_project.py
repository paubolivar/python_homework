from vcf_to_sfs_v2 import Sitefrequency

#Input by user:
vcf_path="gt_I_recoded.vcf.gz"
bed_path="dummy.bed"
pat_out="sfs.out"
n_all_sample = 24
num_reads = 6

#Make collection of snps:
collection = Collect_SNPs(vcf_path,bed_path)

#now make the sfs object
s = SFS(collection.sfs)

#generate final plot
s.plot_sfs()

