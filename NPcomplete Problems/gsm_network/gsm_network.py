# python3

verbose = False
import sys

n, m = map(int, input().split())
edges = [ list(map(int, input().split())) for i in range(m) ]

class Position:
	def __init__(self, varNum, vertex,color):
		self.varNum = varNum
		self.vertex = vertex
		self.color = color

def printClauses(clauses,numVar):
	print(str(len(clauses)) + ' ' + str(numVar))
	for clause in clauses:
		for i in clause:
			sys.stdout.write(str(i))
			sys.stdout.write(' ')
		sys.stdout.write('0 \n')


# This solution prints a simple satisfiable formula
# and passes about half of the tests.
# Change this function to solve the problem.
def printEquisatisfiableSatFormula():
	#print("3 2")
	#print("1 2 0")
	#print("-1 -2 0")
	#print("1 -2 0")		
	clauses = []
	if verbose:
		print(n)
		print(m)
		print(edges)
		print()
	
	#create variables,	 one variable for each color of each vertex
	variables = []
	varCount = 1;
	for i in range(n):
		#for each vertex, append one variable for each color
		for j in range(3):
			variables.append(Position(varCount,i,j))
			varCount += 1

	if verbose:	   
		for i in variables:
			print(i.varNum)
			print(i.vertex)
			print(i.color)
			print()
	
	#conditions
	#each vertex must have exactly one color
	for vertex in range(n):
		#get the variables each color of this vertex
		colors = [i.varNum for i in variables if i.vertex == vertex]

		#add clause that at least one color must be true
		clause = []
		for i in colors:
			clause.append(i)
		clauses.append(clause)

		#add clauses to enforce one color per vertex
		for i in range(3):
			clause = []
			for j in range(3):
				if i != j:
					clause.append(-colors[j])
			clauses.append(clause)
			
	#add clause to enforce that for each edge, the connected vertices have a different color
	for edge in edges:
		#check uniqueness for each color
		for i in range(3):
			clause = []
			for j in edge:
				var = [k.varNum for k in variables if k.vertex == j-1 and k.color == i]
				clause.append(-var[0])
			clauses.append(clause)
				
			
	printClauses(clauses,len(variables))
		
	
		
				
		
			
		
	
	#each vertex must be connected only to vertices of different colors
	
	

printEquisatisfiableSatFormula()
