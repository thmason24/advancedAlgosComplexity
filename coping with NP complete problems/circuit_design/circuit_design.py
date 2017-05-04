# python3
import numpy as np
import threading
import sys
import time

# This code is used to avoid stack overflow issues
sys.setrecursionlimit(10**6) # max depth of recursion
threading.stack_size(2**26)  # new thread will get stack of such size

#n, m = map(int, input().split())
#clauses = [ list(map(int, input().split())) for i in range(m) ]




def checkSolution(solution,clauses):
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
def isSatisfiableNaive(n,m,clauses):
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

def strongConnect(adj,v,SCC,sccVec,index,indexes,lowLink,onStack,stack):
	indexes[v] = index[0]
	lowLink[v] = index[0]
	index[0] += 1
	onStack[v] = True
	stack.append(v)
	#print('v top: ' + str(v))
	for w in adj[v]:
		if indexes[w] == -1:
			strongConnect(adj,w,SCC,sccVec,index,indexes,lowLink,onStack,stack)
			lowLink[v] = min(lowLink[v],lowLink[w])
		elif onStack[w]:
			lowLink[v] = min(lowLink[v],indexes[w])
	
	#print('v: ' + str(v))
	if lowLink[v] == indexes[v]:
		#start new SCC
		#print('start new component')
		SCC.append([])
		while True:
			w = stack.pop()
			SCC[-1].append(w)
			sccVec[w] = len(SCC)
			onStack[w] = False	
			#print('w = ' + str(w))
			#print('v = ' + str(v))		
			if w == v:
				#print('test')
				break
		
	 
def tarjanSCC(adj):
	index = [0]
	indexes = [-1] * len(adj)
	lowLink = [-1] * len(adj)
	sccVec  = [-1] * len(adj)
	onStack = [False] * len(adj)
	stack = []
	SCC = []
	for i in range(len(adj)):
		if indexes[i] == -1:
			strongConnect(adj,i,SCC,sccVec,index,indexes,lowLink,onStack,stack)
	return SCC,sccVec
		
def fastImpGraph(n,m,clauses,verbose,verbose2):
	adj = [[] for _ in range(2*n)]	
	for clause in clauses:
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
		adj[notl1].append(l2)
		adj[notl2].append(l1)
	return adj
		    
				
def isSatisfiable(n,m,clauses,verbose,verbose2,verbose3):

	startFastImp = time.time()
	adj = fastImpGraph(n,m,clauses,verbose,verbose2)
	endFastImp   = time.time()
	if verbose3:
		print('fastImp : ' + str(endFastImp - startFastImp))
		
	startSCC = time.time()
	SCC = tarjanSCC(adj)[0]
	endSCC = time.time()
	if verbose3:
		print('sccTime: ' + str(endSCC - startSCC))
								
	#fast satcheck
	startFastisSat = time.time()
	satisfiable = True
	for vertices in SCC:
		if len(vertices) > 1:
			for i in vertices:
				if i%2 == 0:
					if i+1 in vertices:
						satisfiable = False
						return None
	endFastisSat = time.time()
	if verbose3:
		print('fastisSat Time: ' + str(endFastisSat - startFastisSat))
	
	
	#once it's been shown that no SCC contains a variable and it's negation,  one can find a satisfying assignment
	#since edges are implications,  each variable in an SCC must contain the same value
	#in reverse topological order, assign all literals in an SCC to 1 and negations to zero
	#move up stream in topological order and try to find a 1 implies zero
	#in other words, check to make sure that an upstream variable does not imply it's negation downstream
	
	
	startFastSol = time.time()
	solutionVectorGraph = [-1] * len(adj)
	for vertices in SCC:
		unSetVertices = [i for i in vertices if solutionVectorGraph[i] == -1]	
	endFastSol = time.time()
	if verbose3:
		print('fastsol : '  + str(endFastSol - startFastSol))
	
	startSolution = time.time()
	solutionVectorGraph = [-1] * len(adj)
	for vertices in SCC:
		for j in vertices:
			if solutionVectorGraph[j] == -1:
				solutionVectorGraph[j] = 1
				if j%2 == 0:
					solutionVectorGraph[j+1] = 0
				else:
					solutionVectorGraph[j-1] = 0
	endSolution = time.time()
	if verbose3:
		print('solutionTime: ' + str(endSolution-startSolution))
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
		print(checkSolution(solutionVector,clauses))
	
	return solutionVector	
				
				
def main():

	verbose = False
	verbose2 = False
	verbose3 = True
	showNaive = False
	stressTest = True
	n, m = map(int, input().split())
	clauses = [ list(map(int, input().split())) for i in range(m) ]
	result = isSatisfiable(n,m,clauses,verbose,verbose2,verbose3)
	if result is None:
		print("UNSATISFIABLE")
	else:
		print("SATISFIABLE");
		print(" ".join(str(-i-1 if result[i] else i+1) for i in range(n)))

	if showNaive:
		result = isSatisfiableNaive(n,m,clauses)
		if result is None:
			print("UNSATISFIABLE")
		else:
			print("SATISFIABLE");
			print(" ".join(str(-i-1 if result[i] else i+1) for i in range(n)))

	while stressTest:
		limit = 10000
		n = np.random.randint(1, limit)
		numClauses = np.random.randint(1, limit)
		n= 500000
		numClauses = 500000
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
		
		start = time.time()
		result = isSatisfiable(n,m,clauses,verbose,verbose2,verbose3)
		end  =  time.time()
		
		#resultControl = isSatisfiableNaive(n,m,clauses)
		resultControl = result
	
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
			#print(" ".join(str(-i-1 if result[i] else i+1) for i in range(n)))
	
		if result is None:
			if not resultControl is None:
				print('incorrectly determined to be unsatisfiable')
				print(" ".join(str(-i-1 if resultControl[i] else i+1) for i in range(n)))
				break
		else:
			if not checkSolution(result,clauses):
				print('solution does not satisfy clauses')
				break
		if verbose3:
			print('time: ' + str(end - start))
	
# This is to avoid stack overflow issues
threading.Thread(target=main).start()	