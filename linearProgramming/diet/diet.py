# python3
from sys import stdin
import energy_values as ge #import as gaussian elimination
import copy

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
	maxMetric = 0
	solutionFound = False
	isInfinity = False
	for subset in subsets:
		#form equations for this subset
		subA = []
		subB = []
		for j in subset:
			subA.append(inequalitiesA[j])
			subB.append(inequalitiesB[j])
		equation = ge.Equation(subA,subB)

		
		[b,vertexValid] = ge.SolveEquation(equation)
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
				if metric > maxMetric:
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
    
