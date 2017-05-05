# python3
from itertools import permutations
import time
import numpy as np
import sys
INF = 10 ** 9

def read_data():
    n, m = map(int, input().split())
    graph = [[INF] * n for _ in range(n)]
    for _ in range(m):
        u, v, weight = map(int, input().split())
        u -= 1
        v -= 1
        graph[u][v] = graph[v][u] = weight
    return graph

def print_answer(path_weight, path):
    print(path_weight)
    if path_weight == -1:
        return
    print(' '.join(map(str, path)))


def bin2subset(n):
	return [ind+1  for ind, i in enumerate(str(bin(n)[-1:1:-1])) if int(i) == 1]


def optimal_path(graph):
    n = len(graph)
    best_ans = INF
    best_path = []
    verbose = False
    printTime = False
    startTime = time.time()
    #data structure should be n* 2^n array
    #n=17
    size, perms = n, 2**n
    filler = 0
    C = [[filler for x in range(size)] for y in range(0,perms)] 
    if verbose:
    	print('graph')
    	for i in graph:
    		print(i)
    #set graph that includes 1 and ends at 1 to length zero
    C[0][0] = 0
    #set all other paths that end in 1 to infinity
    for i  in range(1,2**n):
    	C[i][0] = INF
    #iterate through sizes of size 2 to size n
    for s in range(1,n):
    	#print()
    	#print('size ' + str(s+1))
    	sizeCounter = 0
    	sizeArray = []
    	#loop over only odd integers since only they contain vertex 1
    	for i in range(1,2**n,2):
	    	binary = bin(i)[2:]
    		numBits = binary.count('1')
    		#add all permutations of size to the current size array for processing
    		if numBits == s+1:
    			sizeCounter += 1
    			sizeArray.append(i)
    	#print('sizeArray')
    	#for i in sizeArray:
    		#print(i)
    	for S in sizeArray: #iterate over subsets in sizeArray
    		for i in range(1,n): #skip zeroth bit since we never want to remove 1
    			SminusI = S^(1<<i)   #this gives us the set with i removed via xor of 1 rotated i spaces anded with S 
    			if S > SminusI:  #this ensures that i is in S, or else the xor would increase the size
    				minimum = INF
    				for j in range(0,n): 
    					if i != j and S^(1<<j) < S : #need to make sure j is in S and i not equal to j
    						#print('test')
    						#print(graph[i][j])
    						minimum = min(minimum,C[SminusI-1][j] + graph[j][i])  
    						if verbose:
    							print()
    							print('S           ' + str(S))
    							print('S-I         ' + str(SminusI))
    							print('i           ' + str(i))
    							print('j           ' + str(j))
    							print('edge        ' + str(graph[j][i]))
    							print('C_S_I       ' + str(C[S-1][i]))
    							print('C_s-j       ' + str(C[SminusI-1][j]))
    							print('C_s-j+graph ' + str(C[SminusI-1][j] + graph[j][i]))
    							print('min   ' + str(minimum))
    				C[S-1][i] = minimum	
    				if verbose:
    					print('final S ' + str(bin2subset(S)))
    					print('final i ' + str(i+1))
    					print('final C[S,i] ' + str(minimum))		
    	if verbose:
    		print()
    		print('print state')	
    		for ind,i in enumerate(C):
    			if ind%2 == 0:
    				print(str(bin2subset(ind+1)) + ' ' + str(i))		
    if verbose:
    	print()
    	print('end index')
    	for ind,i in enumerate(C):
    		print(str(ind + 1) + ' ' + str(i))

    minPath = []
    minPathLength = INF
    curBesti = 20
    S = 2**n-1
    newS = S
    curBestj = 0
    minPath = []
    subPathLengths = []
    for i in range(n):
    	#print('i ' + str(i))
    	for j in range(1,n):
    		#print('j ' + str(j))
    		if not j in minPath:
    			#print('S ' + str(S))
    			#print(graph[j][curBestj])
    			if C[S-1][j] + graph[j][curBestj] < minPathLength:
    				minPathLength = C[2**n-2][j] + graph[j][0]
    				curBestj = j
    				newS = S^(1<<j)
    	S = newS
    	minPath.append(curBestj)
    	subPathLengths.append(minPathLength)
    	if verbose:
	    	print(minPathLength)
    		print(curBestj)
	    	print(bin2subset(S))

    path = [0]
    for i in list(reversed(minPath))[1:]:
    	path.append(i)
    best_ans = subPathLengths[0]
    best_path = path
        	
    if printTime:
    	print()
    	print('time')
    	print(time.time() - startTime)    	



    if best_ans >= INF:
        return (-1, [])
    return (best_ans, [x + 1 for x in best_path])



def optimal_path_naive(graph):
    # This solution tries all the possible sequences of stops.
    # It is too slow to pass the problem.
    # Implement a more efficient algorithm here.
    n = len(graph)
    best_ans = INF
    best_path = []

    for p in permutations(range(n)):
        cur_sum = 0
        for i in range(1, n):
            if graph[p[i - 1]][p[i]] == INF:
                break
            cur_sum += graph[p[i - 1]][p[i]]
        else:
            if graph[p[-1]][p[0]] == INF:
                continue
            cur_sum += graph[p[-1]][p[0]]
            if cur_sum < best_ans:
                best_ans = cur_sum
                best_path = list(p)

    if best_ans == INF:
        return (-1, [])
    return (best_ans, [x + 1 for x in best_path])
	

if __name__ == '__main__':
	graph = read_data()
	print_answer(*optimal_path(graph))
	print()
	print_answer(*optimal_path_naive(graph))
	stressTest = False
	while stressTest:
		limit = 5
		n = np.random.randint(2, limit)
		graph = [[INF] * n for _ in range(n)]
		for i in range(n):
			for j in range(i,n):
				if i != j:
					if np.random.randint(1,10) > 2:
						graph[i][j] = np.random.randint(1, 40)
						graph[j][i] = graph[i][j]
		
		best = optimal_path(graph)[0]
		bestControl = optimal_path_naive(graph)[0]
		if best != bestControl:
			print()
			print(best)
			print(bestControl)
			print('graph')
			edges = []
			for i in graph:
				print(i)
			for i in range(n):
				for j in range(i,n):
					if i != j and graph[i][j] < INF:
						edges.append([i,j,graph[i][j]])
						#print(str(i+1) + ' ' + str(j+1) + ' ' + str(graph[i][j]))
			print(str(n) + ' ' + str(len(edges)))
			for i in edges:
				sys.stdout.write(str(i[0]+1) + ' ')
				sys.stdout.write(str(i[1]+1) + ' ')
				sys.stdout.write(str(i[2]) + ' ')
				sys.stdout.write('\n')
			break
	
	
	
