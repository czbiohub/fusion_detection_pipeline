#////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////
# script: create_runbatch_config.py
# authors: Lincoln Harris
# date: 10.29.18
#
# Trying to build the input file to give fusionDetectionReflow.rf (required for batch mode run)
#		pandas!!
#////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////
import os
import json
import pandas as pd
pd.options.display.max_colwidth = 500 # module config? 
pd.options.mode.chained_assignment = None  # disable warning message? -- really shouldnt be doing this...

#////////////////////////////////////////////////////////////////////
# writeFunc()
#	Write both samples.csv and config output files
#
#////////////////////////////////////////////////////////////////////
def writeFunc(samples_df):
	# where do you want to write it? 
	out_dir = '../STAR_fus/12.10_run'
	# write samples_df to file
	get_ipython().system(' mkdir -p $out_dir')
	samples_df.to_csv('testOut.csv', index=False)
	# write a config file
	config =     {
		"program": "../../reflow/fusionDetectionReflow.rf",
		"runs_file": "samples.csv"
	}

#////////////////////////////////////////////////////////////////////
# get_fastqs_R1()
#      get full s3 paths for fastq file (R1), then add them to a new col in cells_df
# 
#////////////////////////////////////////////////////////////////////
def get_fastqs_R1(cell):
	s3_location = prefix + cell 
	lines = get_ipython().getoutput('aws s3 ls $s3_location')
	try:
		fq_line = [x for x in lines if x.endswith(('R1_001.fastq.gz','R1_001_merged.fastq.gz'))][0] # get the R1 fastq files
		fq_basename = fq_line.split()[-1]
		retStr = s3_location + fq_basename
		return retStr
	except IndexError:
		return
    
#////////////////////////////////////////////////////////////////////
# get_fastqs_R2()
#	get full s3 paths for fastq file (R2), then add them to a new col in cells_df
#
#////////////////////////////////////////////////////////////////////
def get_fastqs_R2(cell):
	s3_location = prefix + cell 
	lines = get_ipython().getoutput('aws s3 ls $s3_location')
	try:
		fq_line = [x for x in lines if x.endswith(('R2_001.fastq.gz','R2_001_merged.fastq.gz'))][0] # get the R2 fastq files
		fq_basename = fq_line.split()[-1]
		retStr = s3_location + fq_basename
		return retStr
	except IndexError:
		return

#////////////////////////////////////////////////////////////////////
# driver()
#     Gets cell names given a prefix, and sets up dataframe
#
#////////////////////////////////////////////////////////////////////
def driver(prefix): 

    # get all of the cells in a given run directory
	txt = 'runX_cells.txt'
	get_ipython().system(' aws s3 ls $prefix > $txt')

    # read 180226 cell names into a dataframe
	cells_df = pd.read_table(txt, delim_whitespace=True, header=None, names=['is_prefix', 'cell_name'])

    # applying function, and assigning output to new col in cells_df
	cells_df['input_fq_1'] = cells_df['cell_name'].map(get_fastqs_R1) 

    # applying function, and assigning output to new col in cells_df
	cells_df['input_fq_2'] = cells_df['cell_name'].map(get_fastqs_R2) # these map() calls are fucking incredible...
    
    # add a sample_id col
	cells_df['sample_id'] = cells_df.cell_name.str.strip('/') # getting rid of the forward slashes
    
    # building the output dir string
	cells_df['output_prefix'] = 's3://darmanis-group/singlecell_lungadeno/non_immune/nonImmune_fastqs_9.27/STAR-fus_out/' + cells_df.sample_id + '/'
    
    # subset cells_df by only what we want
	cols_to_keep = ['sample_id', 'input_fq_1', 'input_fq_2', 'output_prefix']
	samples_df = cells_df[cols_to_keep]
    
    # rename cols and add ID col
	samples_df.columns = ['sample_id','input_fq1','input_fq2', 'output_dir']
	samples_df['id'] = samples_df['sample_id']

    # rearrange cols
	samples_df = samples_df[['id', 'sample_id', 'input_fq1', 'input_fq2', 'output_dir']]

	return samples_df

#////////////////////////////////////////////////////////////////////
# main()
#	Main logic here. THIS WOULD HAVE BEEN MUCH MORE EFFICIENT WITH A PD.MAP() CALL!!
#					NO MORE FOR LOOPS WHEN PANDAS IS INVOLVED!!
#////////////////////////////////////////////////////////////////////

bucketPrefixes = 's3://darmanis-group/singlecell_lungadeno/non_immune/nonImmune_fastqs_9.27/'
f = 'myCells.txt'
get_ipython().system(' aws s3 ls $bucketPrefixes > $f')
    
# read run prefixes into a pandas df
runs_df = pd.read_table(f, delim_whitespace=True, header=None, names=['is_prefix', 'run_name'])
    
# add a full_path col
runs_df['full_path'] = 's3://darmanis-group/singlecell_lungadeno/non_immune/nonImmune_fastqs_9.27/' + runs_df['run_name']
    
big_df = pd.DataFrame() # init empty dataframe

for i in range(0, len(runs_df.index)-1): # -2 to get rid of STAR-fus_out folder
	global prefix # dont like this -- bad coding practice
	prefix = runs_df['full_path'][i]
	print(prefix)
	curr_df = driver(prefix)
	toConcat = [big_df, curr_df]
	big_df = pd.concat(toConcat)
	print(big_df.shape)
	writeFunc(big_df) # bc im nervous as FUCK 

writeFunc(big_df)

#////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////