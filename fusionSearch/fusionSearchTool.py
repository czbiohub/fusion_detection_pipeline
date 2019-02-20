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

	cwd = os.getcwd()
	path = cwd + '/' + 'fusion_prediction_files/' + cellFile
	
	curr_fusions = pd.read_csv(path, sep='\t')
	
	fusionsList = list(curr_fusions['#FusionName'])

	if str(FOI) in fusionsList:
		outputRow = pd.DataFrame([[cellFile, 1]], columns=['cellName', 'fusionPresent_bool'])
	else:
		outputRow = pd.DataFrame([[cellFile, 0]], columns=['cellName', 'fusionPresent_bool'])

	return outputRow

#////////////////////////////////////////////////////////////////////
# main()
#
#
#////////////////////////////////////////////////////////////////////

pos_test = 'CD24P4--QPRT'
queryStr = 'ALK--EML4'
queryStr_rev = 'EML4--ALK'

cellFiles = os.listdir('./fusion_prediction_files')
cellFiles_df = pd.DataFrame(data=cellFiles, columns=['name']) # need to convert to df before apply call

outputDF_init = pd.DataFrame(columns=['cellName', 'fusionPresent_bool']) 	

outputRows = cellFiles_df.apply(searchFunc, axis=1, args=(pos_test,))
outputDF = outputDF_init.append(outputRows, ignore_index=True)
outputDF.to_csv('testOut.csv', index=False)

#////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////
