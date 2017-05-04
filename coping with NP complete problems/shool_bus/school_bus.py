# python3
from itertools import permutations
import time
import numpy as np
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
	return [ind  for ind, i in enumerate(str(bin(n)[-1:1:-1])) if int(i) == 1]


def optimal_path(graph):
    n = len(graph)
    best_ans = INF
    best_path = []
    
    startTime = time.time()
    #data structure should be n* 2^n array
    #n=17
    size, perms = n, 2**n
    C = [[0 for x in range(size)] for y in range(perms)] 
    #print(Matrix)
    C[0][0] = 0
    for s in range(1,n):
    	sizeCounter = 0
    	sizeArray = []
    	#loop over only odd integers since only they contain vertex 1
    	for i in range(1,2**n,2):
	    	binary = bin(i)[2:]
    		numBits = binary.count('1')
    		#add all permutations of size to the current size array for processing
    		if numBits == s:
    			sizeCounter += 1
    			sizeArray.append(i)
    			#set C(S,1) to infinity
    			C[s][0] = INF    		
    	for S in sizeArray: #iterate over subsets in sizeArray
    		binary = bin(S)[2:]
    		for i in range(1,n): #skip 1
    			SminusI = S^(1<<i)   #this gives us the set with i removed via xor of 1 rotated i spaces anded with S 
    			if S > SminusI:  #this ensures that i is in S, or else the xor would increase the size
    				for j in range(1,n):
    					if i != j:
    						C[S][i] = min(C[S][i],C[SminusI][j] + graph[i][j])    			
    			
    		
    	print(sizeCounter)
    print('time')
    print(time.time() - startTime)    	

    #print(allsubs)
    
        	
    	#S = bin2subset(s)
    	#for i in range(s):
    		#if i != 1:
    			#for j in range(s):
    				#if i != j:
    					#A = C[i]
    					#get subset of S-{i}
    					#B = s^(1 << i)
    	
    	
    		 
    #iterate through subsets in increasing size using conversion of integers to bits 
    
    #for i in range(2**n):
    	#print(i)
    	#convert to subset
    	#print(bin(i))
    	#print(bin2subset(i))
    	#remove one bit
    	#print()
    	#B = i^(1 << 2)
    	#print(B)
    	#print(bin2subset(B))

    if best_ans == INF:
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
	print_answer(*optimal_path(read_data()))
	#print()
	#print_answer(*optimal_path_naive(read_data()))
