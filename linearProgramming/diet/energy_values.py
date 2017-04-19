# python3

EPS = 1e-6
PRECISION = 20

class Equation:
    def __init__(self, a, b):
        self.a = a
        self.b = b

class Position:
    def __init__(self, column, row):
        self.column = column
        self.row = row
        self.valid = True

def ReadEquation():
    size = int(input())
    a = []
    b = []
    for row in range(size):
        line = list(map(float, input().split()))
        a.append(line[:size])
        b.append(line[size])
    return Equation(a, b)

def SelectPivotElement(a, used_rows, used_columns):
	# This algorithm selects the first free element.
	# You'll need to improve it to pass the problem.
	pivot_element = Position(0, 0)
	#print('test2')
    #find leftmost non zero which is unused
	while used_rows[pivot_element.row]:
		pivot_element.row += 1	
	while used_columns[pivot_element.column]:
		pivot_element.column += 1	
	#get first non zero value among unused rows
	#print(a)
	#print(pivot_element.row)
	#print(pivot_element.column)
	while a[pivot_element.row][pivot_element.column] == 0:
		#print('test4')
		if pivot_element.row < len(a)-1:
			pivot_element.row += 1
		else:
			pivot_element.valid = False
			break
		#print(pivot_element.row)
		#print(pivot_element.column)
		
	return pivot_element

def SwapLines(a, b, used_rows, pivot_element):
    a[pivot_element.column], a[pivot_element.row] = a[pivot_element.row], a[pivot_element.column]
    b[pivot_element.column], b[pivot_element.row] = b[pivot_element.row], b[pivot_element.column]
    used_rows[pivot_element.column], used_rows[pivot_element.row] = used_rows[pivot_element.row], used_rows[pivot_element.column]
    pivot_element.row = pivot_element.column;

def ProcessPivotElement(a, b, pivot_element):
    # Write your code here
    #scale row
    b[pivot_element.row] = b[pivot_element.row]/a[pivot_element.row][pivot_element.column]
    a[pivot_element.row] = [i/a[pivot_element.row][pivot_element.column] for i in a[pivot_element.row]]
    #subtract from other rows to make then zeros
    for rowInd,row in enumerate(a):
    	if rowInd != pivot_element.row:
    		scaleFactor = float(row[pivot_element.column])
    		if scaleFactor != 0:
    			row = [i/scaleFactor for i in row]
    			b[rowInd] = b[rowInd]/scaleFactor
    			row = [a - b for a, b in zip(row, a[pivot_element.row])]
    			b[rowInd] = b[rowInd] - b[pivot_element.row]
    			
    			a[rowInd] = row
    			#rescale row by it's index to make it's primary number 1
    			reScale = a[rowInd][rowInd]
    			a[rowInd] = [i/reScale for i in a[rowInd]]
    			b[rowInd] = b[rowInd]/reScale
    			#a[rowInd] = row

def MarkPivotElementUsed(pivot_element, used_rows, used_columns):
    used_rows[pivot_element.row] = True
    used_columns[pivot_element.column] = True
    
def printA(a,b):
	for ind,i in enumerate(a):
		print(str(i) + '   ' + str(b[ind]))

def SolveEquation(equation):
    a = equation.a
    b = equation.b
    size = len(a)

    used_columns = [False] * size
    used_rows = [False] * size
    for step in range(size):
        pivot_element = SelectPivotElement(a, used_rows, used_columns)
        if not pivot_element.valid:
        	print('test3')
        	return [0, False] #return false validity
        #print('pivot element : ' + str(pivot_element.row) + ' '  + str(pivot_element.column))
        #print('a before swap')
        #printA(a,b)
        SwapLines(a, b, used_rows, pivot_element)
        #print('a after swap')
        #printA(a,b)
        ProcessPivotElement(a, b, pivot_element)
        #print('a after process')
        #printA(a,b)
        #print()
        MarkPivotElementUsed(pivot_element, used_rows, used_columns)

    return [b, True]  #return b and validity

def PrintColumn(column):
    size = len(column)
    for row in range(size):
        print("%.20lf" % column[row])

if __name__ == "__main__":
    equation = ReadEquation()
    solution = SolveEquation(equation)
    PrintColumn(solution)
    exit(0)
