#!/usr/bin/python
'''Project name: vcf_to_sfs


This project estimates and makes a plot of the SFS from a vcf. These information can be filtered for 
different purposes in terms of number of alleles samples, min numbe rof reads covered, class of mutation, genomic region.

input files: 
1.  vcf file
2.	BED files to filter for example repetitive regions.

input parameters by user:
1. num_reads: min number of reads for each individual.
2. num_individuals: number of genotyped individuals.

output1: 
1. plots.

This project has three main classes: Sitefrequency, Collect_SNPs, Sfs.

Example files in the example directory

usage example: python final_proj.py dummy_recoded.vcf.gz dummy.bed 8 1
'''

import os
import random
import tabix
import pandas as pd
import numpy as np
from ggplot import ggplot, aes, geom_bar

class Sitefrequency(object): 
	''' The instances of this class are the sites in the VCF file. Input line in vcf file.'''
	def __init__(self, record, num_reads=6):
		self.num_reads = num_reads
		self.scaf = record[0] # first column of vcf file
		self.pos = record[1] # second column of vcf
		self.ancestral = record[3] # (ancestral allele) fourth column of vcf
		self.derived = record[4] # (derived alleles) fifth columns of vcf
		self.num_alleles , self.derived_count =	[i for i in self.get_genotypes(record, self.num_reads)]		#number of genotyped individuals (alleles) that passes filetring for num_reads for that site.
		#print self.scaf, self.pos, self.ancestral, self.derived, self.num_alleles , self.derived_count

		if (self.ancestral == "A" or self.ancestral == "T") and (self.derived == "G" or self.derived == "C"):
			self.mutcat = "WS" 
		elif (self.ancestral == "G" or self.ancestral == "C") and (self.derived == "A" or self.derived == "T"):
			self.mutcat = "SW" 
		elif (self.ancestral == "G" or self.ancestral == "C") and (self.derived == "G" or self.derived == "C"):
			self.mutcat = "SS" 
		else: 
			self.mutcat = "WW"
	
	def get_genotypes(self, record, num_reads): 
		''' Gets eache site's attributes from vcf file. Filters out sites that have lower number of reads than the number speficied by the user.
		The user needs to specify min number of reads and also the number of alleles to sample'''
		derived_count = 0
		num_gen = 0
		genotypes = []
		for col in record[9:]: #for each column in the line starting in column 10
			info = col.split(':') #split the column by ':' 	  	
			if info[0] != "./." and int(info[1]) > int(self.num_reads):#if the second element of this column is smller than num_reads specified by user (then the site is excluded) 
				gen = info[0].split('/') #split the firt element of this column (the two values for the genotype)
				for element in gen: #for each genotype (there are two)
					if element == '1' or element =='0': #discard '.' and maybe a second derived allele
						genotypes.append(element)
						#print genotypes
		return len(genotypes), genotypes.count('1')      		    	

class Collect_SNPs(object): 
    '''Collects all sites (of class Sitefrequency) that pass desired creiteria and puts them into a SNP collection
    Input are the VCF, GFF, BED files. Output is an object of class Collect_SNPs that contains the desired sites.
    An instance of this class is a list of sites.'''
    def __init__(self, coll_snps=[]): 
        self.coll_snps = coll_snps
        if len(self.coll_snps)>0: 
            #check that all the sites are of type SiteFrequency if input is not a vcf.
            assert all([type(site) ==  Sitefrequency for site in self.coll_snps] )
      		
    def get_SNPS(self, vcf_path, bed_path):
        '''get the actual collection of sdesired sites'''
        self.vcf_path = vcf_path
        self.bed_path = bed_path
        print "Analyzing vcf file %s" % self.vcf_path
        print "Analyzing bed file %s" % self.bed_path
        
        self.coll_snps = []
        for line in open(self.bed_path, 'r'):
        	line = line.strip("\n").split("\t")
        	start = int(line[1])
        	end = int(line[2])
        	print start,end
        	tb = tabix.open(self.vcf_path)
        	records = tb.queryi(0, start, end)
        	for record in records:
        		site = Sitefrequency(record) #assign this site as an instance of class Sitefrequency().
        		if site.ancestral == "N": #if ancestral state is not defined then discard site.
        			continue
        		self.coll_snps.append(site)#append site to the collection.

    def get_filter(self, mutcat):
    	'''filters the collection accordying to the mutation category'''
    	filtered_coll_snps = [site for site in self.coll_snps if site.mutcat == mutcat]
    	return Collect_SNPs(filtered_coll_snps)

    def get_SFS(self, n_all_sample):
        n_all_sample = int(n_all_sample)
        sfs_list = [0] * (n_all_sample+1)
        for site in  self.coll_snps: #here we iterate over the sites in the collection of snps, where can access the site's attributes.
            if site.num_alleles<=n_all_sample: #Discard sites if num alleles covered is lowewr than the min specified by user.
                continue
            list_alleles = ([1]*site.derived_count) + ([0]* (site.num_alleles-site.derived_count))
            sample = random.sample(list_alleles,n_all_sample)#subsample the num_alleles specified by user.
            derived_count_sample =sample.count(1)
            sfs_list[derived_count_sample]+=1
        return sfs_list

class SFS(object):
	'''This class takes as input an SFS and outputs a plot'''
	def __init__(self, sfs):
		self.sfs = sfs
		self.num_sites = sum(self.sfs)
	
	def plot_sfs(self, pat_out):
		df = pd.DataFrame({"freq":[i for i in range(1,len(self.sfs))], "sfs" : np.array(self.sfs[1:len(self.sfs)])})
		print df
		pl = ggplot(df, aes(x="freq", weight="sfs")) + geom_bar()
		pl.save(pat_out)