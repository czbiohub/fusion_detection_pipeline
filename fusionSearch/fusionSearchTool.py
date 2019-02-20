#////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////
# script: fusionSearchTool.py
# author: Lincoln 
# date: 2.19.19
#
#	Hey you! yes you! Do you have a shit-ton of tsv files that contain
#	the fusions identified by STAR-fusion, on a per-cell basis?? 
#	then this tool is the one for you!! so step right up
#
#	run this puppy like so: 
#
#		python3 fusionSearchTool.py [mode] [ROI]
#
#			where [ROI] is the fusion you want to search for, separated
#			by some motherfuckin dashes, 
#				ie. ALK--EML4
#////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////
import pandas as pd
import os
import sys

#////////////////////////////////////////////////////////////////////
# searchFunc_ANY()
#	can i define a func for searching for ANY partner to a given 
#	query gene? 
#
#			IN PROGRESS
#////////////////////////////////////////////////////////////////////
def searchFunc_ANY(row, GOI):
	cellFile = row['name']
	cellName = cellFile.split('_')[0] + '_' + cellFile.split('_')[1]

	cwd = os.getcwd()
	path = cwd + '/' + 'fusion_prediction_files/' + cellFile
	
	curr_fusions = pd.read_csv(path, sep='\t')
	
	fusionsList = list(curr_fusions['#FusionName'])

	outputRow = pd.DataFrame([[cellName, 0]])

	for item in fusionsList:
		if GOI in item:
			outputRow = pd.DataFrame([[cellName, 1]])
			return outputRow

	return outputRow

#////////////////////////////////////////////////////////////////////
# searchFunc()
#	doing the actual searching from here -- turns the #FusionName col
#	into a list, then searches that fucker for the FOI, 
#////////////////////////////////////////////////////////////////////
def searchFunc(row, FOI):
	cellFile = row['name']
	cellName = cellFile.split('_')[0] + '_' + cellFile.split('_')[1]

	cwd = os.getcwd()
	path = cwd + '/' + 'fusion_prediction_files/' + cellFile
	
	curr_fusions = pd.read_csv(path, sep='\t')
	
	fusionsList = list(curr_fusions['#FusionName'])

	if str(FOI) in fusionsList:
		outputRow = pd.DataFrame([[cellName, 1]])
	else:
		outputRow = pd.DataFrame([[cellName, 0]])

	return outputRow

#////////////////////////////////////////////////////////////////////
# main()
#
#
#////////////////////////////////////////////////////////////////////
global colNames

mode = sys.argv[1]
queryStr = sys.argv[2]

print(' ')
print('query: %s' % queryStr)
print(' ')

outFileStr = queryStr + '.query.out.csv'
colNames = ['cellName', 'fusionPresent_bool']

cellFiles = os.listdir('./fusion_prediction_files')
cellFiles_df = pd.DataFrame(data=cellFiles, columns=['name']) # need to convert to df before apply call

print('running...')

if mode == 0: # standard two-gene mode

	queryStrSplit = queryStr.split('--')
	queryStrRev = queryStrSplit[1] + '--' + queryStrSplit[0]

	outputRows = cellFiles_df.apply(searchFunc, axis=1, args=(queryStr,))
	outputRows_list = list(outputRows) # for some reason need to convert to a list before concatting
	outputDF = pd.concat(outputRows_list, ignore_index=True)

	outputRows_rev = cellFiles_df.apply(searchFunc, axis=1, args=(queryStrRev,))
	outputRows_rev_list = list(outputRows_rev) # for some reason need to convert to a list before concatting
	outputDF_rev = pd.concat(outputRows_rev_list, ignore_index=True)

	outputDF.columns = colNames
	outputDF_rev.columns = colNames

	outputDF_comb = pd.DataFrame(columns=colNames)
	outputDF_comb['cellName'] = outputDF['cellName']
	outputDF_comb['fusionPresent_bool'] = outputDF['fusionPresent_bool'] + outputDF_rev['fusionPresent_bool']
	outputDF_comb.to_csv(outFileStr, index=False)

else: # single gene mode 
	outputRows = cellFiles_df.apply(searchFunc_ANY, axis=1, args=(queryStr,))
	outputRows_list = list(outputRows) # for some reason need to convert to a list before concatting
	outputDF = pd.concat(outputRows_list, ignore_index=True)
	outputDF.to_csv(outFileStr, index=False)

print('done!')

#////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////
