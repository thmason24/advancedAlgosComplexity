# python3
from sys import stdin
from scipy.optimize import linprog
import numpy as np
import copy


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
	while abs(a[pivot_element.row][pivot_element.column]) < 0.001:
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
    #print(pivot_element.row)
    #print(pivot_element.column)
    #for i in a:
   # 	print(i)
    #print(b)
    #print(a[pivot_element.row][pivot_element.column])
    #print(b[pivot_element.row])
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
    			if reScale != 0:
	    			a[rowInd] = [i/reScale for i in a[rowInd]]
    				b[rowInd] = b[rowInd]/reScale
    			else:
    				#fill b vector with nones
    				pass
    				#b[rowInd] = None
    				
    			
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
        	#print('test3')
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


def getSubsets(n,m):
	#return subsets of size m
	subsets = []
	subsets.append([])
	subsets.append([0])
	for i in range(1,n+m+1):
		subsets1 = copy.deepcopy(subsets)
		subsets2 = copy.deepcopy(subsets)

		for k in range(len(subsets1)):
			subsets1[k].append(i)
		subsets = subsets1 + subsets2
		
	sizeMsubsets = []
	for i in subsets:
		if len(i) == m:
			sizeMsubsets.append(i)
	return sizeMsubsets
			

  
def solve_diet_problem(n, m, A, b, c):  
	# Write your code here
	# linear programming of the form Ax < b
	# we want to maximize the c*x

	inequalitiesA = []
	inequalitiesB = []
	for ind, i in enumerate(A):
		inequalitiesA.append(i)
		inequalitiesB.append(b[ind])
	#add constraints for x > 0
	for i in range(m):
		vector = [0] * m
		vector[i] = -1 #negative to express amount > 0 using the same format as the regular inequalites
		inequalitiesA.append(list(vector))
		inequalitiesB.append(0)
	#add inequality for very large solution to check infinity
	inequalitiesA.append([1] * m)
	inequalitiesB.append(10**9)
		
	subsets = getSubsets(n, m)
	
	#for each subset of inequalities, perform gaussian elimination to solve for a vertex
	printA(inequalitiesA,inequalitiesB)
	maxMetric = -float('inf')
	solutionFound = False
	isInfinity = False
	for subset in subsets:
		#form equations for this subset
		subA = []
		subB = []
		for j in subset:
			subA.append(inequalitiesA[j])
			subB.append(inequalitiesB[j])
		print()
		printA(subA,subB)
		equation = Equation(subA,subB)

		
		[b,vertexValid] = SolveEquation(equation)
		if vertexValid:
			#check if solution honors all inequalities
			isSolution = True
			
			for ind,inequality in enumerate(inequalitiesA):
				if not sum([inequality[k]*b[k] for k in range(len(inequality))]) <= inequalitiesB[ind]:
					isSolution = False
					break
			if isSolution:
				solutionFound = True
				#calculate metric
				metric = sum([b[i]*c[i] for i in range(m)])
				print()
				print('its a solution!!!!!!!!!!!!!!!!!!')
				print(b)
				print(metric)
				print()
				if metric > maxMetric:
					print('and its better')
					maxMetric = metric
					bestAnswer = list(b)
					#check if last inequality (the check for infinity) is one of the vertexes for the current max
					if len(inequalitiesA)-1 in subset:
						isInfinity = True
					else:
						isInfinity = False 
					
	ansx = [0] * m
	if not solutionFound:
		anst = -1
	elif isInfinity:
		anst = 1
	else:
		anst = 0
		ansx = bestAnswer

	return [anst, ansx]

n, m = list(map(int, stdin.readline().split()))
A = []
for i in range(n):
	A += [list(map(int, stdin.readline().split()))]
b = list(map(int, stdin.readline().split()))
c = list(map(int, stdin.readline().split()))

anst, ansx = solve_diet_problem(n, m, A, b, c)


if anst == -1:
	print("No solution")
if anst == 0:  
	print("Bounded solution")
	print(' '.join(list(map(lambda x : '%.18f' % x, ansx))))
if anst == 1:
	print("Infinity")

if True:
	linprog_res = linprog(-np.array(c), A_ub=np.array(A), b_ub=np.array(b), options={'tol': 1e-3})
	if linprog_res.status == 3:
		print('Infinity')
	elif linprog_res.status == 2:
		print('No solution')
	elif linprog_res.status == 0:
		solution_x = linprog_res.x
		print('x_ref =', ' '.join(list(map(lambda x: '%.18f' % float(x), solution_x))))
		print('Bounded solution')    
