# python3
import sys

verbose = False
verbose2 = False

if verbose2:
	from satispy import Variable, Cnf 
	from satispy.solver import Minisat


n, m = map(int, input().split())
edges = [ list(map(int, input().split())) for i in range(m) ]

class Position:
	def __init__(self, varNum, vertex, pos):
		self.varNum = varNum
		self.vertex = vertex
		self.pos = pos

def printClauses(clauses,numVar,verbose):
	print(str(len([i for i in clauses if not isinstance(i, str)])) + ' ' + str(numVar))
	for clause in clauses:
		if isinstance(clause, str):
			if verbose:
				print(clause)
		else:
			for i in clause:
				sys.stdout.write(str(i))
				sys.stdout.write(' ')
			sys.stdout.write('0 \n')
	if verbose:
		count = 0
		for j in [i for i in clauses if not isinstance(i, str)]:
			if not isinstance(j,str):
				count += len(j)
		print('total count ' + str(count))
			
def genExpression(clauses):
	expr = ''
	for indClause,clause in enumerate(clauses):
		if not isinstance(clause, str):
			
			for ind,j in enumerate(clause):
				expr = expr + str(j)
				expr = expr + ' ' 
				if not ind == len(clause)-1:
					expr = expr + ' | '
			if not indClause == len(clauses)-1: 
				expr = expr + '& '
	return expr
		
def printVariables(variables):
	print('Variables matrix')
	print('ind vert pos')
	for i in variables:
		print(str(i.varNum) + '   ' + str(i.vertex) + '    ' + str(i.pos))
	print()

def printEdges(edges):
	if len(edges) == 0:
		print('no edges')
	else:
		print('Edges')
	for i in edges:
		print(str(i[0]) + ' ' + str(i[1]))
	print()

def printEquisatisfiableSatFormula():

	#create variables
	variables = []
	varCount = 1
	for i in range(n):
		#for each vertex, append one variable for each position in the path
		#the number of positions equals the number of vertices in the graph for n^2 total variables
		for j in range(n):
			variables.append(Position(varCount,i,j))
			varCount += 1
	if verbose:
		printVariables(variables)
		printEdges(edges)
		
	clauses = []
	for i in range(n):  #loop over rooms
	
		#enforce that every room must be visited
		#get all the variables corresponding to this position and ensure one of them is true
		vars = [j.varNum for j in variables if j.vertex == i]
		#create an or clause of these variables and add it
		clauses.append('enforce at least one visit')
		clause = []
		for j in vars:
			clause.append(j)
		clauses.append(clause)
		
		clauses.append('enforce only one visit')
		#enforce that no room can be visited more than once
		#loop over positions for this room and ensure it has no more that 1 position
		for j in range(n):
			for k in range(n):
				#for each pair of position variable ensure that at most of them is true
				if j < k:
					clause = []
					clause.append(-vars[j])
					clause.append(-vars[k])
					clauses.append(clause)
					
	#enforce every path position is used
	clauses.append('enforce all path positions used')
	for i in range(n):
		vars = [j.varNum for j in variables if j.pos == i]
		clause = []
		for j in vars:
			clause.append(j)
		clauses.append(clause)
	clauses.append('each position used only once')
	for i in range(n):
		vars = [j.varNum for j in variables if j.pos == i]
		for j in range(n):
			for k in range(n):
				#for each pair of position variable ensure that at most of them is true
				if j < k:
					clause = []
					clause.append(-vars[j])
					clause.append(-vars[k])
					clauses.append(clause)	
		
					
	#use edges to determine which transitions are not allowed
	#for example, if no edge exists between room 3 and room4, we must insert a condition that
	#room3 cannot be adjacent to room 4  (room3 in position i implies room 4 cannot be in position 5 or 3)
	clauses.append('Enforce no path if no edge')

	#loop through all possible connections
	for i in range(n):
		for j in range(n):
			if i != j:
				#determine if edge exists
				edgeExists = False
				for edge in edges:
					if i+1 == edge[0] and j+1 == edge[1]:
						edgeExists = True
					if i+1 == edge[1] and j+1 == edge[0]:
						edgeExists = True
				#print(edgeExists)
				#if no edge, add a clause excluding this connection for each step
				if not edgeExists:
					for step in range(1,n):
						#get variable for these edges and these steps
						var1 =  [k.varNum for k in variables if k.vertex == i and k.pos == step][0]
						var2 =  [k.varNum for k in variables if k.vertex == j and k.pos == step-1][0]
						#print(var1)
						#print(var2)
						clause = []
						clause.append(-var1)
						clause.append(-var2)
						clauses.append(clause)

	printClauses(clauses,len(variables),verbose)
	#print(genExpression(clauses))
	if verbose2:
		solver = Minisat()
		solution = solver.solve(eval(genExpression(clauses)))

		if solution.success:
			print('Found a solution:')
		else:
			print('The expression cannot be satisfied')
printEquisatisfiableSatFormula()
