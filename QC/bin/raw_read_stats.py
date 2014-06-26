#! /usr/bin/env python
import sys
import os
sys.path.append('../src')
sys.path.append('../../fast5_file_manipulation/src')
from fast5 import fast5File
from optparse import OptionParser
import glob
import logging
import csv
from Bio import SeqIO
import numpy as np
import operator

## Takes a directory of basecalled ONT fast5 files or fastafiles and returns some basic stats 
## on the number of bases, reads, quality scores etc. 
parser = OptionParser()
parser.description = """
Calculates some basic stats on ONT fastq reads"""
parser.add_option("-d", "--dir", dest="directory",
                  help="path to directory containing fast5 or fastq files")
# parser.add_option("-o", "--out", dest="outdir",
#                   help="path to output directory",default="./")
(opt, args) = parser.parse_args()
if opt.directory is None:
    parser.print_help()
    sys.exit()

### Get all the files in the directory 
fqFilelist = glob.glob(opt.directory+"/*.fq")
fast5Filelist = glob.glob(opt.directory+"/*.fast5") 
if fast5Filelist:
	logging.error("Haven't written fast5 handler code yet...")
## Make the output directories
def makeDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
def makeOutFileName(fastq):
	outdir = "/".join(fastq.split("/")[:-2]) + "/stats/"
	makeDir(outdir)
	outname = fastq.split("/")[-1].split(".fq")[0] + "_raw_read_stats.dat"
	return outdir + outname

## Define some parameters
qualbins = range(60)

header = ["id","length","meanQualScore","sdQualScore"]
logging.info("Analysing fastq files")
for fastq in fqFilelist:
	## Storing values for histograms
	runningQualityScoreHist = [0]*len(qualbins)
	## File names 
	outfile_name = makeOutFileName(fastq)
	logging.info("%s " % outfile_name.split('/')[-1])
	## Write stats to file
	with open(outfile_name,'w') as outfile:
		writer = csv.writer(outfile,delimiter="\t")
		writer.writerow(header)
		for record in SeqIO.parse(fastq, "fastq-sanger"):
			qualityScores = record.letter_annotations["phred_quality"]
			row = [record.id,len(record.seq),np.mean(qualityScores),np.std(qualityScores)]
			hist,bin_edges=np.histogram(qualityScores,bins=qualbins)
			runningQualityScoreHist = [i+j for i,j in zip(hist,runningQualityScoreHist)]
			writer.writerow(row)

for fast5 in fast5Filelist:
	f5 =  fast5File(filepath=f)
	


