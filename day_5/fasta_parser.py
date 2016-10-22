# Fasta Parser
# Paulina

import os
import re
import pandas as pd
import numpy as np
from ggplot import ggplot, aes, geom_density

class FastaParser(object):
    '''This class parses fasta files.'''
    def __init__(self, pat=None):
        self.pat = pat

        if not os.path.exists(self.pat):
        	raise IOError("File does not exist")
        if self.pat == None:
        	raise TypeError("No file path provided")

        self.num = ["".join(value) for key, value in self.dic().items()]
        self.dict = {key: "".join(value) for key, value in self.dic().items()}
        self.lengt_dist = self.length_dist("test1.pdf")
        self.count = len(self)

    def __len__(self):
        '''returns the length of the sequence.'''
        c = 0
        for line in self.opened_file():
            if line.startswith('>'):
            	c += 1
        return c

    def __getitem__(self, item):
        '''Makes object iterable so we can use it as a normal dictionary.
        Returns the value of the dictionary per each key 
        (as index via self.num or as key via self.dict).'''
        if type(item) == int:
            return self.num[item]
        else:
            return self.dict[item]

    def opened_file(self):
        return open(self.pat, 'r')

    def dic(self):
        '''Returns a dictionary for each sequence.'''
        seq_dict = {}
        for line in self.opened_file():
            line = line.rstrip('\n')
            if line.startswith('>'):
                    tag = line[1:]
            if tag not in seq_dict:
                seq_dict[tag] = []
                continue
            seq_dict[tag].append(line)
        return seq_dict

    def extract_length(self, seq_len):
        '''Returns a list with the sequences that are shorter than specified length (seq_len).'''
        return [i for i in self.num if len(i) < seq_len]

    def length_dist(self, pat_out="genes_lengths.png"):
        '''Gets a list of sequence lengths, creates a dataframe and plots it using ggplot.
        Then saves the file in specified path.'''
        len_ditribution = [len(i) for i in self.num]
        df = pd.DataFrame({"record_length" : np.array(len_ditribution)})
        pl = ggplot(df, aes(x="record_length")) + geom_density()
        pl.save(pat_out)
