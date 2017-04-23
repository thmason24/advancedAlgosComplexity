# python3
import sys


n, m = map(int, input().split())
edges = [ list(map(int, input().split())) for i in range(m) ]

class Position:
	def __init__(self, varNum, vertex, pos):
		self.varNum = varNum
		self.vertex = vertex
		self.pos = pos

def printClauses(clauses,numVar):
	print(str(len(clauses)) + ' ' + str(numVar))
	for clause in clauses:
		for i in clause:
			sys.stdout.write(str(i))
			sys.stdout.write(' ')
		sys.stdout.write('0 \n')

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
	clauses = []
	for i in range(n):  #loop over rooms
	
		#enforce that every room must be visited
		#get all the variables corresponding to this position and ensure one of them is true
		vars = [j.varNum for j in variables if j.pos == i]
		#create an or clause of these variables and add it
		clause = []
		for j in vars:
			clause.append(j)
		clauses.append(clause)
		
		#enforce that no room can be visited more than once
		#loop over positions for this room and ensure it has no more that 1 position
		for j in range(n):
			for k in range(n):
				#for each pair of position variable ensure that at most of them is true
				if j != k:
					clause = []
					clause.append(-vars[j])
					clause.append(vars[k])
					clauses.append(clause)
					
	#use edges to determine which transitions are not allowed
	#for example, if no edge exists between room 3 and room4, we must insert a condition that
	#room3 cannot be adjacent to room 4  (room3 in position i implies room 4 cannot be in position 5 or 3)
	
	#loop through all possible connections
	for i in range(n):
		for j in range(n):
			if i != j:
				#determine if edge exists
				edgeExists = False
				for edge in edges:
					if i == edge[0] and j == edge[1]:
						edgeExists = True
					if i == edge[1] and j == edge[0]:
						edgeExists = True
				print(edgeExists)
				#if no edge, add a clause excluding this connection for each step
				if not edgeExists:
					for step in range(2,n):
						#get variable for these edges and these steps
						var1 =  [k.varNum for k in variables if k.vertex == i and k.pos == step][0]
						var2 =  [k.varNum for k in variables if k.vertex == j and k.pos == step-1][0]
						clause = []
						clause.append(-var1)
						clause.append(-var2)
						clauses.append(clause)

	#printClauses(clauses,len(variables))

printEquisatisfiableSatFormula()
