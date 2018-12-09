import xlsxwriter
plotList=[]

with open('plot_file.txt','r') as f:
	for entry in f.readlines():
		line = entry.split(' ')
		listToAppend=[]
		for term in line:
			listToAppend.append(term)
		plotList.append(listToAppend)


for item in plotList:
	print item

workbook = xlsxwriter.Workbook('plot.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})

# number_format = workbook.add_format({'num_format': '$#,##0'})
worksheet.write('A1', 'Run', bold)
worksheet.write('B1', 'Query ID', bold)
worksheet.write('C1', 'Recall', bold)
worksheet.write('D1', 'Precision', bold)

row = 1
col = 0

for run, queryid, recall,precsion in (plotList):
     worksheet.write_string(row, col,run)
     worksheet.write_string(row, col + 1, queryid)
     worksheet.write_string(row, col + 2, recall)
     worksheet.write_string(row, col + 3, precsion)
     row += 1


workbook.close()