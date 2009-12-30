#!/usr/bin/python

def buildLists():
	f = open('btriangle.txt')
	rows = []
	for line in f:
		row = []
		for value in line.split():
			item = {'value':int(value)}
			if len(rows) > 0:		#not first row
				if len(row) > 0:			#not first item
					item['parent1'] = rows[-1][len(row) - 1]

				try:
					item['parent2'] = rows[-1][len(row)]
				except:
					pass
			row.append(item)
		rows.append(row)
	return rows

def fillMaxes(rows):
	rows[0][0]['maxvalue'] = rows[0][0]['value']		#initialize first row
	rows[0][0]['maxparent'] = rows[0][0]

	for row in rows[1:]:
		for item in row:
			try:
				p1max = item['parent1']['maxvalue'] + item['value']
			except:
				p1max = 0
			try:
				p2max = item['parent2']['maxvalue'] + item['value']
			except:
				p2max = 0

			
			if p1max > p2max:
				item['maxvalue'] = p1max
				item['maxparent'] = item['parent1']
			else:
				item['maxvalue'] = p2max
				item['maxparent'] = item['parent2']

def genHtml(rows):
	highlight = getMaxItem(rows)	#initial highlighted item
	output = []
	for row in reversed(rows):
		vals= []
		for item in row:
			if item == highlight:
				vals.append("<span style='color:red'>%s</span>" %
						item['value'])
				highlight = item['maxparent']
			else:
				vals.append(str(item['value']))
		output.append( " ".join(vals) )
	
	output.reverse()
	print "<center>" + "<br>\n".join(output) + "</center>"

def getMaxItem(rows):
	maxitem = rows[-1][0]
	for item in rows[-1]:
		if item['maxvalue'] > maxitem['maxvalue']:
			maxitem = item
	return maxitem

def main():
	rows = buildLists()
	fillMaxes(rows)
	maxitem = getMaxItem(rows)
	print "The maximal path is of value %s" % maxitem['maxvalue']
	genHtml(rows)

if __name__ == "__main__":
	main()
