#////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////
# script: fusionDetectionPipelineManual.py
# author: Lincoln 
# date: 1.9.19
# 
# FUCK REFLOW
# usage:
#		ipython fusionDetectionPipelineManual.py
#////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////
import os
import json
import pandas as pd
pd.options.display.max_colwidth = 500
pd.options.mode.chained_assignment = None 

#////////////////////////////////////////////////////////////////////
# get_fastq1()
#	what does this fucker do? 
#////////////////////////////////////////////////////////////////////

def get_fastq1(cell):
    s3_location = prefix + cell 
    lines = get_ipython().getoutput('aws s3 ls $s3_location') 
    
    try:
    	fastq_line = [x for x in lines if x.endswith('_R1_001.fastq.gz')][0] # get the fastq file, specifically
    	fastq_basename = fastq_line.split()[-1]
    except IndexError:
    	return('dummy') # think this will work so long as i return something

    return s3_location + fastq_basename

#////////////////////////////////////////////////////////////////////
# get_fastq2()
#	what does this fucker do? 
#////////////////////////////////////////////////////////////////////

def get_fastq1(cell):
    s3_location = prefix + cell 
    lines = get_ipython().getoutput('aws s3 ls $s3_location') 
    
    try:
    	fastq_line = [x for x in lines if x.endswith('_R2_001.fastq.gz')][0] # get the fastq file, specifically
    	fastq_basename = fastq_line.split()[-1]
    except IndexError:
    	return('dummy') # think this will work so long as i return something

    return s3_location + fastq_basename

#////////////////////////////////////////////////////////////////////
# driver()
#	what does this fucker do? 
#////////////////////////////////////////////////////////////////////

def driver():
	txt = 'runX_cells.txt'
	get_ipython().getoutput('aws s3 ls $prefix > $txt')
    
	# read into a pandas dataframe
	cells_df = pd.read_table(txt, delim_whitespace=True, header=None, names=['is_prefix', 'cell_name'])

	cells_df['input_fastq1'] = cells_df['cell_name'].map(get_fastq1)
	cells_df['input_fastq2'] = cells_df['cell_name'].map(get_fastq2)
	cells_df['sample_id'] = cells_df.cell_name.str.strip('/') # get rid of forward slashes and add 'sample_id' col

	# get current fastqs
	get_ipython().system('aws s3 cp s3://darmanis-group/singlecell_lungadeno/non_immune/nonImmune_fastqs_9.27/170125/A10_1001000293/A10_1001000293_R1_001.fastq.gz .')
	get_ipython().system('aws s3 cp s3://darmanis-group/singlecell_lungadeno/non_immune/nonImmune_fastqs_9.27/170125/A10_1001000293/A10_1001000293_R2_001.fastq.gz .')

	# run STAR-fus, from docker container
	get_ipython().system('sudo docker run -v `pwd`:/data --rm trinityctat/ctatfusion /usr/local/src/STAR-Fusion/STAR-Fusion --left_fq /data/*_R1_001.fastq.gz --right_fq /data/*_R2_001.fastq.gz --genome_lib_dir /data/ctat_genome_lib_build_dir -O /data/StarFusionOut --FusionInspector validate --examine_coding_effect --denovo_reconstruct')

	# remove current fastqs
	get_ipython().system('rm *.fastq.gz')

#////////////////////////////////////////////////////////////////////
# main()
#	what does this fucker do? 
#////////////////////////////////////////////////////////////////////

# get list of all the runs
bucketPrefixes = 's3://darmanis-group/singlecell_lungadeno/non_immune/nonImmune_fastqs_9.27/'
f = 'myRuns.txt'
get_ipython().system('aws s3 ls $bucketPrefixes > $f')

# read run prefixes into a pandas df
runs_df = pd.read_table(f, delim_whitespace=True, header=None, names=['is_prefix', 'run_name'])
    
# add a full_path col
runs_df['full_path'] = 's3://darmanis-group/singlecell_lungadeno/non_immune/nonImmune_fastqs_9.27/' + runs_df['run_name']

for i in range(0, len(runs_df.index)-1): # -2 bc i have two vcf out folders
	global prefix # dont like this
	prefix = runs_df['full_path'][i]
	print(prefix)
	driver(prefix)

#////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////
