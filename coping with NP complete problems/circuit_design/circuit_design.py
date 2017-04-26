# python3
n, m = map(int, input().split())
clauses = [ list(map(int, input().split())) for i in range(m) ]

verbose = False

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

def dfs(adj, used, order, x):
    used[x] = 1
    for i in adj[x]:
        if not used[i]:
            dfs(adj,used,order,i)
    order.insert(0,x)
    return
            
def toposort(adj):
	#find strongly connected components and provide topoligical order
    used = [0] * len(adj)
    order = []
    for i in range(len(adj)):
        if not used[i]:
            dfs(adj,used,order,i)
    return order       
            
def defineImplicationGraph():
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
	
	
	#add test edge
	#edges.append([0,1])
	#edges.append([1,0])
	
	if verbose:
		print('variables')
		print(vertices)
		print()
		print('clauses')
		for i in clauses:
			print(i)
		print()
		print('edges')
		for i in edges:
			print(i)
	
	#convert to adjacency list
	adj = []
	for i in vertices:
		adjEntree = []
		for j in edges:
			if j[0] == i:
				adjEntree.append(j[1])
		adj.append(adjEntree)
	
	if verbose:
		print()
		print('adjacency list')
		for i in adj:
			print(i)
	
	return adj
				
	

def isSatisfiable():
	adj = defineImplicationGraph()
	if verbose:
		print()
		print('find Strongly connected components')
	#get topo order
	topoOrder = toposort(adj)
	sscOrder = [-1] * len(adj)
	curSCCorder = 0
	#explore from last item in toporder to find scc components via explore
	inGraph = [True] * len(adj)
	while any(inGraph):
		#explore from last sink still in the graph
		#get lowest topo order still in graph
		for i in range(len(adj)):
			if inGraph[topoOrder[-(i+1)]]:
				sink = topoOrder[-(i+1)]
				break
		if sink == 5 and False:
			break
		visited = [False] * len(adj)
		explore(adj,sink,visited,inGraph)
		#assign visited to current sccOrder
		for i in range(len(adj)):
			if visited[i]:
				sscOrder[i] = curSCCorder
				inGraph[i]  = False
		curSCCorder += 1
	if verbose:
		print()
		print('sscOrder')
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
	
	solutionVector = [-1] * len(adj)
	for i in range(max(sscOrder)+1):
		vertices = [j for j in range(len(adj)) if sscOrder[j] == i]
		for j in vertices:
			if solutionVector[j] == -1:
				solutionVector[j] = 1
				if j%2 == 0:
					solutionVector[j+1] = 0
				else:
					solutionVector[j-1] = 0
	return solutionVector
				
				
		
	

result = isSatisfiable()
if result is None:
    print("UNSATISFIABLE")
else:
    print("SATISFIABLE");
    print(" ".join(str(-i-1 if result[i] else i+1) for i in range(n)))

if False:
	result = isSatisfiableNaive()
	if result is None:
		print("UNSATISFIABLE")
	else:
		print("SATISFIABLE");
		print(" ".join(str(-i-1 if result[i] else i+1) for i in range(n)))
