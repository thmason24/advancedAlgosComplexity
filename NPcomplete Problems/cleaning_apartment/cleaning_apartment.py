# python3
n, m = map(int, input().split())
edges = [ list(map(int, input().split())) for i in range(m) ]

class Position:
	def __init__(self, varNum, vertex, pos):
		self.varNum = varNum
		self.vertex = vertex
		self.pos = pos

def printClause(clause):
	print(clause)

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

	#enforce that every room must be visited
	for i in range(n):
		#get all the variables corresponding to this position and ensure one of them is true
		vars = [j.varNum for j in variables if j.pos == i]
		#create an or clause of these variables and add it
		clause = []
		for j in vars:
			clause.append(j)
		printClause(clause)
	
	#enforce that each room can only be visited once
	
	#enforce that vertices with adjacent positions must be connected on the graph through an edge



printEquisatisfiableSatFormula()
