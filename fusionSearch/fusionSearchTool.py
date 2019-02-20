#////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////
# script: fusionSearchTool.py
# author: Lincoln 
# date: 2.19.19
#
#////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////
import pandas as pd
import os

#////////////////////////////////////////////////////////////////////
# searchFunc()
#	what does this fucker do? 
#
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

pos_test = 'CD24P4--QPRT'
queryStr = 'ALK--EML4'
queryStr_rev = 'EML4--ALK'

colNames = ['cellName', 'fusionPresent_bool']

cellFiles = os.listdir('./fusion_prediction_files')
cellFiles_df = pd.DataFrame(data=cellFiles, columns=['name']) # need to convert to df before apply call

outputRows = cellFiles_df.apply(searchFunc, axis=1, args=(pos_test,))
outputRows_list = list(outputRows) # for some reason need to convert to a list before concatting

outputDF = pd.concat(outputRows_list, ignore_index=True)
outputDF.to_csv('testOut.csv', index=False)

#////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////
