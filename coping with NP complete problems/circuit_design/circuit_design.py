# python3
import numpy as np
import threading
import sys

# This code is used to avoid stack overflow issues
sys.setrecursionlimit(10**6) # max depth of recursion
threading.stack_size(2**26)  # new thread will get stack of such size

#n, m = map(int, input().split())
#clauses = [ list(map(int, input().split())) for i in range(m) ]




def checkSolution(solution):
	satisfied = True
	for clause in clauses:
		clauseSatisfied = False
		if solution[abs(clause[0]) - 1] == (clause[0] < 0):
			clauseSatisfied = True
		if solution[abs(clause[1]) - 1] == (clause[1] < 0):
			clauseSatisfied = True
		if not clauseSatisfied:
			satisfied = False
			break
	return satisfied		


# This solution tries all possible 2^n variable assignments.
# It is too slow to pass the problem.
# Implement a more efficient algorithm here.
def isSatisfiableNaive():
    for mask in range(1<<n):
        result = [ (mask >> i) & 1 for i in range(n) ]
        formulaIsSatisfied = True
        for clause in clauses:
            clauseIsSatisfied = False
            if result[abs(clause[0]) - 1] == (clause[0] < 0):
                clauseIsSatisfied = True
            if result[abs(clause[1]) - 1] == (clause[1] < 0):
                clauseIsSatisfied = True
            if not clauseIsSatisfied:
                formulaIsSatisfied = False
                break
        if formulaIsSatisfied:
            return result
    return None


def explore(adj,x,visited,inGraph):
	visited[x] = True
	for i in adj[x]:
		if not visited[i] and inGraph[i]:
			explore(adj,i,visited,inGraph)
	return visited

def dfs(adj, visited, postOrder,clock, x):
	#print('visiting ' + str(x))
	visited[x] = True
	for i in adj[x]:
		if not visited[i]:
			dfs(adj,visited,postOrder,clock,i)      
	clock[0] += 1
	postOrder[x] = clock[0]  
	return
    
def number_of_strongly_connected_components(adj,adjr,n,m,clauses,verbose,verbose2):
    result = 0
    postOrder = [0] * len(adj)
    #initialize visited with removed list
    visited   =  [False] * len(adj)
    clock = [0]
    #find a sink by finding a source in the reverse graph
    #a vertex in the source compoenent will have a higher postorder than
    #those that are not sources
    for i in range(len(adjr)):
        if not visited[i]:
            dfs(adjr,visited,postOrder,clock,i)
    
    #get reverse post order
    reversePostOrder = np.argsort(postOrder)[::-1]

    #reinit visisted
    visited   =  [False] * len(adj)
    compAssigned = [-1]  * len(adj)  
    #run dfs on the real adjency list in reverse sort order.  count every time a dfs starts fresh from the top on an unvisited node
    if verbose2:
	    print('reverse post order  ' +str(reversePostOrder))
    for i in reversePostOrder:
        if not visited[i]:
            result += 1
            dfs(adj,visited,postOrder,clock,i)
            for j in range(len(adj)):
            	if compAssigned[j] == -1 and visited[j]:
            		compAssigned[j] = result
        
    return compAssigned
               
def defineImplicationGraph(n,m,clauses,verbose,verbose2):
	#create vertices from variables
	#range twice n for a positive and negative of each variable
	vertices = range(2*n)
	#add implication edges
	edges = []
	for clause in clauses:
		#for each clause, add an edge from not u to v, and from not v to u
		if len(clause) == 2:
			if clause[0] > 0:
				l1 = 2*(abs(clause[0])-1)
				notl1 = 2*(abs(clause[0])-1)+1
			else:
				l1 = 2*(abs(clause[0])-1)+1
				notl1 = 2*(abs(clause[0])-1)
			#and for l2
			if clause[1] > 0:
				l2 = 2*(abs(clause[1])-1)
				notl2 = 2*(abs(clause[1])-1)+1
			else:
				l2 = 2*(abs(clause[1])-1)+1
				notl2 = 2*(abs(clause[1])-1)			
		
			edges.append([notl1,l2])
			edges.append([notl2,l1])
		else:
			if clause[0] > 0:
				edges.append([2*(abs(clause[0])-1)+1,2*(abs(clause[0])-1)])
			else:
				edges.append([2*(abs(clause[0])-1),2*(abs(clause[0])-1)+1])
	
	if verbose:
		print('variables')
		print(vertices)
		print()
		print('clauses')
		for i in clauses:
			print(i)
			
	if verbose2:
		print()
		print('edges')
		for i in edges:
			print(i)
			
	#convert to adjacency list
	adj = [[] for _ in range(2*n)]
	for (a, b) in edges:
		adj[a].append(b)
	#reverse graph
	adjr = [[] for _ in range(2*n)]
	for (a, b) in edges:
		adjr[b].append(a)
        
	if verbose2:
		print()
		print('adjacency list')
		for i in adj:
			print(i)
			
		print()
		print('reverse adj list')
		for i in adjr:
			print(i)
	
	return adj, adjr
				
def isSatisfiable(n,m,clauses,verbose,verbose2):
	adj,adjr = defineImplicationGraph(n,m,clauses,verbose,verbose2)
	sscOrder = number_of_strongly_connected_components(adj,adjr,n,m,clauses,verbose,verbose2)
								
	if verbose:
		print()
		print('sccOrder')
		print(sscOrder)
	
	satisfiable = True
	#check if any strongly connected component has a variable and it's negation
	for i in range(max(sscOrder)+1):
		vertices = [j for j in range(len(adj)) if sscOrder[j] == i]
		#check if component has any variable with it's negation
		for i in range(0,len(adj),2):
			if i in vertices and i+1 in vertices:
				satisfiable = False
				return None

	
	#once it's been shown that no SCC contains a variable and it's negation,  one can find a satisfying assignment
	#since edges are implications,  each variable in an SCC must contain the same value
	#in reverse topological order, assign all literals in an SCC to 1 and negations to zero
	#move up stream in topological order and try to find a 1 implies zero
	#in other words, check to make sure that an upstream variable does not imply it's negation downstream
	
	solutionVectorGraph = [-1] * len(adj)
	for i in range(max(sscOrder)+1):
		vertices = [j for j in range(len(adj)) if sscOrder[j] == i]
		for j in vertices:
			if solutionVectorGraph[j] == -1:
				solutionVectorGraph[j] = 1
				if j%2 == 0:
					solutionVectorGraph[j+1] = 0
				else:
					solutionVectorGraph[j-1] = 0
	if verbose:				
		print('solutionVector Graph')
		print(solutionVectorGraph)
	#convert graph solution to solutionVector
	solutionVector = [-1] * n
	for i in range(n):
		if solutionVectorGraph[i*2] == 1:
			solutionVector[i] = 0
		else:
			solutionVector[i] = 1
	if verbose:
		print('solutionVector')
		print(solutionVector)	
	
	if verbose:
		print(checkSolution(solutionVector))
	
	return solutionVector	
				
				
def main():

	verbose = False
	verbose2 = False
	showNaive = False
	stressTest = False
	n, m = map(int, input().split())
	clauses = [ list(map(int, input().split())) for i in range(m) ]
	result = isSatisfiable(n,m,clauses,verbose,verbose2)
	if result is None:
		print("UNSATISFIABLE")
	else:
		print("SATISFIABLE");
		print(" ".join(str(-i-1 if result[i] else i+1) for i in range(n)))

	if showNaive:
		result = isSatisfiableNaive()
		if result is None:
			print("UNSATISFIABLE")
		else:
			print("SATISFIABLE");
			print(" ".join(str(-i-1 if result[i] else i+1) for i in range(n)))

	while stressTest:
		limit = 8
		n = np.random.randint(1, limit)
		numClauses = np.random.randint(1, limit)
		print()
		print('numVar:     ' + str(n))
		print('numClauses: ' + str(numClauses))
	
	
		#gen clauses
		clauses = []
		for i in range(numClauses):
			clause = []
			for i in range(2):
				sign = np.random.randint(0, 2)
				if sign == 0:
					literal = np.random.randint(1, n+1)
				else:
					literal = np.random.randint(-n,0)
				clause.append(literal)
			clauses.append(clause)
		
	
		result = isSatisfiable()
		resultControl = isSatisfiableNaive()
	
		print()
		if showNaive:
			print('clauses')
			for i in clauses:
				print(i)
		print()
		if result is None:
			print("UNSATISFIABLE")
		else:
			print("SATISFIABLE");
			print(" ".join(str(-i-1 if result[i] else i+1) for i in range(n)))
	
		if result is None:
			if not resultControl is None:
				print('incorrectly determined to be unsatisfiable')
				print(" ".join(str(-i-1 if resultControl[i] else i+1) for i in range(n)))
				break
		else:
			if not checkSolution(result):
				print('solution does not satisfy clauses')
				break
	
	
# This is to avoid stack overflow issues
threading.Thread(target=main).start()	