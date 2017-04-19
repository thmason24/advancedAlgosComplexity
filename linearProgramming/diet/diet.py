# python3
from sys import stdin
import energy_values as ge #import as gaussian elimination
import copy

def getSubsets(n,m):
	#return subsets of size m
	subsets = []
	subsets.append([])
	subsets.append([0])
	for i in range(1,n+m):
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
	print('n ' + str(n))
	print('m ' + str(m))
	for ind, i in enumerate(A):
		print(str(i) + str(b[ind]))
	print
	print(b)
	print(c)
	
	print()
	
	print('assemle list of inequalities')
	inequalitiesA = []
	inequalitiesB = []
	for ind, i in enumerate(A):
		inequalitiesA.append(i)
		inequalitiesB.append(b[ind])
	#add constraints for x > 0
	for i in range(m):
		vector = [0] * m
		vector[i] = 1
		inequalitiesA.append(list(vector))
		inequalitiesB.append(0)
	
	for ind, i in enumerate(inequalitiesA):	
		print(str(i) + ' ' + str(inequalitiesB[ind]))
		
	
	print()
	print('subsets')
	subsets = getSubsets(n, m)
	print(subsets)
	
	#for each subset of inequalities, perform gaussian elimination to solve for a vertex
	for i in subsets:
		#form equations for this subset
		subA = []
		subB = []
		#print(i)
		for j in i:
			subA.append(inequalitiesA[j])
			subB.append(inequalitiesB[j])
		print('equations')
		equation = ge.Equation(subA,subB)
		print(equation.a)
		print(equation.b)
		print('test1')
		print(ge.SolveEquation(equation))
	
	
	
	#there are at most 8 inequalities and 8 variables
	#8 extra inequalities if you count each c >= 0
	#at vertices, some of the inequalities are equalities and so can be solved with 
	#gaussian elimination
	
	#choose m of the m+n inequalities and find their vertices using gaussian elimination treating them
	#as equalities
	
	
	
	
	
	
	
	print('find a starting point')
	print('add equations one at a time and optimize.')
	
		
	
	
	print('start simplex')
	
	
	

	return [0, [0] * m]

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
    
