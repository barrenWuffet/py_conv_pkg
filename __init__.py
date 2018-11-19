import numpy
import pandas
import collections
import operator
import sys

def prof_df(df):
	if type(df) is not pandas.DataFrame:
		raise ValueError("input is not a DataFrame")
		sys.exit(1)
	prof = pandas.DataFrame(list(range(1,len(df.columns.values) + 1)), columns = ['row_num'])
	prof['col_name'] = df.columns.values
	prof = prof.set_index('col_name')
	prof['row_cnt'] = len(df.index)
	prof['uniq_val'] = df.apply(lambda row:len(row.unique()), axis = 0)
	prof['na_cnt'] = df.apply(lambda row:sum(row.apply(lambda x: (pandas.isna(x)) | (str(x) == 'NA'))), axis = 0)
	prof['blank_cnt'] = df.apply(lambda row:sum(row.apply(lambda x:(not pandas.isna(x)) & (str(x) == ""))), axis = 0)
	prof['top_val'] = df.apply(lambda row:row.value_counts().index[0], axis = 0)
	prof['na_pct'] = round(prof['na_cnt']/prof['row_cnt'], 4)
	prof['blank_pct'] = round(prof['blank_cnt']/prof['row_cnt'], 4)
	prof['top_5_val_pct'] = df.apply(lambda row: round(numpy.nansum(row.value_counts().reset_index(drop = True)[0:5] if len(row.value_counts().index) >= 5 else row.value_counts().reset_index(drop = True)[0:len(row.value_counts().index)])/len(row),4))
	return prof

def rankTab(x):
	rank =  pandas.DataFrame(pandas.Series(x).value_counts()).reset_index(level = 0, inplace = True)
	rank.columns = ['x', 'Freq']
	return rank