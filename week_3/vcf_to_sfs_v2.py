'''Project name: vcf_to_sfs


This project analyses diversity data. It will take genetic variant information per site from may individuals 
and process it to get summarized diversity information. It is useful to get diversity estimates from a variant file
in the forms of population genetic statistics such as pi, theta_w and sfs. These information can be filtered for 
different purposes in terms of number of alleles samples, class of mutation, genomic region.

input: 
1.  vcf file
2.	BED files to filter for example repetitive regions.

input by user:
1. num_reads: min number of reads an individual need to have in order to be sampled.
2. num_individuals: number of genotyped individuals.

output1: 
1. report/plots.


This project has three main classes: Sitefrequency, Collect_SNPs, Sfs.


'''

import os
import re
import random
import tabix
import pandas as pd
import numpy as np
from ggplot import ggplot, aes, geom_bar

class Sitefrequency(object): 
	''' The instances (objects) of this class are the sites in the VCF file. Input line in vcf file.'''
	def __init__(self, record, num_reads=6):
		self.num_reads = num_reads
		self.scaf = record[0] # first column of vcf file
		self.pos = record[1] # second column of vcf
		self.ancestral = record[3] # (ancestral allele) fourth column of vcf
		self.derived = record[4] # (derived alleles) fifth columns of vcf
		self.num_alleles , self.derived_count =	[i for i in self.get_genotypes(record, self.num_reads)]		#number of genotyped individuals (alleles) that passes filetring for num_reads for that site.
		#print self.scaf, self.pos, self.ancestral, self.derived, self.num_alleles , self.derived_count
		self.mutcat = "test"
		if (self.ancestral == "A" or self.ancestral == "T") and (self.derived == "G" or self.derived == "C"):
			self.mutcat = "WS" 
		elif (self.ancestral == "G" or self.ancestral == "C") and (self.derived == "A" or self.derived == "T"):
			self.mutcat = "SW" 
		elif (self.ancestral == "G" or self.ancestral == "C") and (self.derived == "G" or self.derived == "C"):
			self.mutcat = "SS" 
		else: 
			self.mutcat = "WW" 	

#	def __getitem__(self, item):
#		'''Makes object iterable'''
#		return self.num_alleles[item] #, self.derived_count[item]

	def get_genotypes(self, record, num_reads): 
		'''Filters out sites that have lower number of reads than the number speficied by the user.
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
    '''Collects all sites (of class Sitefrequency) that pass desired creiteria and puts them into a SNPlist
	Input are the VCF, GFF, BED files. Output is a list (maybe also writen to a file) that contains the desired sites.
    An instance of this class is a list of sites.'''
    def __init__(self, coll_snps=[], mutcat=""): 
        self.coll_snps = coll_snps
        self.coll_len = len(self.coll_snps)
        if len(self.coll_snps)>0: 
            #check that all the sites are of type SiteFrequency
            assert all([type(site) ==  Sitefrequency for site in self.coll_snps] )
            self.coll_snps = self.get_filter(mutcat)
            self.sfs = self.get_SFS()
        else:
        	self.coll_snps = self.get_SNPS(vcf_path, bed_path)
        	self.coll_len = len(self.coll_snps)
        	self.sfs = self.get_SFS()
	

    def get_SNPS(self, vcf_path=vcf_path, bed_path=bed_path):
        self.vcf_path = vcf_path
        self.bed_path = bed_path
        print "Analyzing vcf file %s" % self.vcf_path
        print "Analyzing bed file %s" % self.bed_path
        
        self.coll_snps = []
        for line in open(self.bed_path, 'r'):
        	line = line.strip("\n").split("\t")
        	start = int(line[1])
        	end = int(line[2])
        	tb = tabix.open(self.vcf_path)
        	records = tb.queryi(0, start, end)
        	for record in records:
        		#print record
        		site = Sitefrequency(record) #assign this site as an instance of class Sitefrequency().
        		if site.ancestral == "N": #if ancestral state is not defined then discard site.
        			continue
        		self.coll_snps.append(site)
        	return self.coll_snps

    def get_filter(self, mutcat):
    	self.coll_snps = [site for site in self.coll_snps if site.mutcat == mutcat]
    	return self.coll_snps

    def get_SFS(self):
		#n_all_sample = 24
		sfs_list = [0] * (n_all_sample+1)
		for site in  self.coll_snps: #here we iterate over the sites in the collection of snps, where can access the site's attributes.
			#print site.num_alleles, n_all_sample
			if site.num_alleles<=n_all_sample:
			    #raise Exception
			    continue
			list_alleles = ([1]*site.derived_count) + ([0]* (site.num_alleles-site.derived_count))
			sample = random.sample(list_alleles,n_all_sample)
			derived_count_sample =sample.count(1)
			#print sample
			#print derived_count_sample
			sfs_list[derived_count_sample]+=1
		return sfs_list

class SFS(object):
	'''This class takes as input a collection of SNPs and outputs plot'''
	def __init__(self, sfs, pat_out="sfs.eps"):
		self.sfs = sfs
		self.pat_out = pat_out
		self.num_sites = sum(self.sfs)
		self.num_alleles = n_all_sample
		#self.plot = self.plot_sfs()
	
	def plot_sfs(self):
		df = pd.DataFrame({"freq":[i for i in range(1,(self.num_alleles))], "sfs" : np.array(self.sfs[1:self.num_alleles])})
		print df
		pl = ggplot(df, aes(x="freq", weight="sfs")) + geom_bar()
		pl.save(self.pat_out)


#collect.sfs.plot 