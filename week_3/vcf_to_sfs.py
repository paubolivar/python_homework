'''Project name: vcf_to_sfs

This project andalyses diversity data. It will take genetic variant information pero site from may individuals 
and process it to get summarized diversity information. It is useful to get diversity estimates from a variant file
in the forms of population genetic statistics such as pi, theta_w and sfs. These information can be filtered for 
different purposes in terms of number of alleles samples, class of mutation, genomic region.
It will summarize diversity data to get 

input: 
1.  vcf file
2.	Intersection with GFF file to be able to extract info for genes, or intergenic regions.
3.	Intersection to BED files to filter repetitive regions.

output1: csv
cols: crom (contig), position, genomic_region, ancestral_alleles, derived_alleles, frequency_class

output2: csv
sfs for certain desired parameters.

main ojbects: input files

Class Sitefrequency(): Process each site (line) in the vcf file.
	
	Attributes: 
		Path to vcf
		chr (contig) number
		position
		Ancestral alleles
		Derived alleles
		genomic_region (for example: coding, intergenic)
		selection (selected vs non selected site)
		Min number of genotyped individuals (input by user)
		Number of genotyped individuals (x)
		Frequency class of the site: number of ind with the derived variant (y)
		path outfile

	Methods:
		open(): read file
		__len__(): of vcf file
		__item__(): make object iterable
		get_numsites: get total number of sites that passed fiter 
		genomic_region(): read GFF file to get info regarding the genomic region where each site is.
		sel_or_neu(): read file with info regarding if a site is putatively evolving under neutrality of under selection
					(for example 0 and 4 fds or conserved elements info) 
		get_frequency(): counts how many ind have derived allele and how many have ancestral (or total).
		write_to_file():

Class Sfs(): 
	Attributes: 
		thetaw
		pi
		sfs
		afs
	Methods: 
		open(): read file
		__len__(): of vcf file
		__item__(): make object iterable
		get_stats(): gets thetaw, pi, or other pop gen stats
		get_sfs(): get sfs (counts) as dictionary 
		get_asf(): get afs (frequency)	as dictionary

		If there is time, sfs and afs could be estimated separetley for each mutation category.

This code will be used by Bob in order to estimate pop gen statistics and the sfs from a vcf file.
He need to be able to estimate this for different functional categories (genes, introns, intergenic regions, etc).
Also, he wants to get the selected and neutral sfs for coding regions (and other putatively functional sites) 
and he want to be able to differenciate between different mutation categories ( for example : transitions and transversions),
and wants to have separate estimates for these categoies. Finally, he want to be able to plot these. 


'''

