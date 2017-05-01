#uses python3

import sys
import threading

# This code is used to avoid stack overflow issues
sys.setrecursionlimit(10**6) # max depth of recursion
threading.stack_size(2**26)  # new thread will get stack of such size
verbose = False

class Vertex:
    def __init__(self, weight):
        self.weight = weight
        self.children = []


def ReadTree():
    size = int(input())
    tree = [Vertex(w) for w in map(int, input().split())]
    for i in range(1, size):
        a, b = list(map(int, input().split()))
        tree[a - 1].children.append(b - 1)
        tree[b - 1].children.append(a - 1)
    return tree


def dfs(tree, vertex, parent, score):
	if verbose:
		print('vertex: ' + str(vertex))
		print('parent: ' + str(parent))
		print('children: ' + str(tree[vertex].children))
	for child in tree[vertex].children:
		if child != parent:
			if verbose:
				print('descend')
			dfs(tree, child, vertex, score)
	if verbose:
		print('post vertex: ' + str(vertex))
	m1 = tree[vertex].weight
	for i in tree[vertex].children:
		if i != parent:
			for j in tree[i].children:
				if j != i and j != vertex:
					if verbose:
						print('vertex        : ' + str(vertex))
						print('children      : ' + str(i))
						print('grandchildren : ' + str(j))
						print(m1)
					m1 = m1 + score[j]
					if verbose:
						print(m1)
	m0 = 0
	for i in tree[vertex].children:
		if i != parent:
			m0 = m0 + score[i]

	score[vertex] = max(m0,m1)
	if verbose:
		print('m1 ' + str(m1))
		print('m0 ' + str(m0))
		print('score: ' + str(score))
					
	    
    # This is a template function for processing a tree using depth-first search.
    # Write your code here.
    # You may need to add more parameters to this function for child processing.


def MaxWeightIndependentTreeSubset(tree):
    size = len(tree)
    if size == 0:
        return 0
    score = [float('inf')] * size
    dfs(tree, 0, -1,score)
    # You must decide what to return.
    return score[0]


def main():
    tree = ReadTree();
    weight = MaxWeightIndependentTreeSubset(tree);
    print(weight)


# This is to avoid stack overflow issues
threading.Thread(target=main).start()
