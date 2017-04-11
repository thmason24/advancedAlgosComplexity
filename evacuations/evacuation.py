# python3
import queue
import sys

class Edge:

    def __init__(self, u, v, capacity):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = 0

# This class implements a bit unusual scheme for storing edges of the graph,
# in order to retrieve the backward edge for a given edge quickly.
class FlowGraph:

    def __init__(self, n):
        # List of all - forward and backward - edges
        self.edges = []
        # These adjacency lists store only indices of edges in the edges list
        self.graph = [[] for _ in range(n)]

    def add_edge(self, from_, to, capacity):
        # Note that we first append a forward edge and then a backward edge,
        # so all forward edges are stored at even indices (starting from 0),
        # whereas backward edges are stored at odd indices.
        forward_edge = Edge(from_, to, capacity)
        backward_edge = Edge(to, from_, 0)
        self.graph[from_].append(len(self.edges))
        self.edges.append(forward_edge)
        self.graph[to].append(len(self.edges))
        self.edges.append(backward_edge)

    def size(self):
        return len(self.graph)

    def get_ids(self, from_):
        return self.graph[from_]

    def get_edge(self, id):
        return self.edges[id]

    def add_flow(self, id, flow):
        # To get a backward edge for a true forward edge (i.e id is even), we should get id + 1
        # due to the described above scheme. On the other hand, when we have to get a "backward"
        # edge for a backward edge (i.e. get a forward edge for backward - id is odd), id - 1
        # should be taken.
        #
        # It turns out that id ^ 1 works for both cases. Think this through!
        self.edges[id].flow += flow
        self.edges[id ^ 1].flow -= flow


def read_data():
    vertex_count, edge_count = map(int, input().split())
    graph = FlowGraph(vertex_count)
    for _ in range(edge_count):
        u, v, capacity = map(int, input().split())
        graph.add_edge(u - 1, v - 1, capacity)
    return graph


def findMinPath(graph,from_,to):
    #perform a bfs from 'from' until we find 'to'.   this path is a candidate shortest path for edmonds carp 
    #we'll need a queue for bfs initialized at 'from'
    q = queue.Queue()    
    q.put(from_)
    #initialize all prev values to -1
    prev = graph.size() * [-1]
    visited = graph.size() * [False]
    while not q.empty():
        u = q.get()
        for i in graph.get_ids(u):  #get edge ids from this vertex
            #get edge
            edge = graph.get_edge(i)
            
            if edge.capacity - edge.flow > 0 and not visited[edge.v]: #only process the edge if there is unfilled capacity
                if edge.v == to:
                    #if 'to' is discovered then find path and return
                    path = []
                    #add first edge to path
                    path.append(i)
                    while edge.u != from_: #add prev edges until return to source

                        #update prevEdge with prevEdge of u
                        prevEdgeID = prev[edge.u]
                        #add edge to path
                        path.append(prevEdgeID)
                        edge = graph.get_edge(prevEdgeID)

                    return path
                else:
                    #place edge 'to' in queue
                    visited[edge.v] = True
                    q.put(edge.v)
                    #update prev edge for v with edge id
                    prev[edge.v] = i 

    #if 'to' is never found,  return -1
    return -1




def max_flow(graph, from_, to):
    flow = 0
    #ford-fulkerson with edmonds karp
    while True:  # repeat until break due to no path available on residual
        #find minimum path in graph from s - t (source to sink) with the smallest number of edges
        minPath = findMinPath(graph,from_,to)
        #break if no minPath found
        if minPath == -1:
            break
        #find min flow that can be added
        minFlow = float('inf')
        for i in minPath:
            edge = graph.get_edge(i)
            if edge.capacity - edge.flow < minFlow:
                minFlow = edge.capacity - edge.flow
        #add minimum flow to the path
        for i in minPath:
            graph.add_flow(i,minFlow)

    #find edges that go to 'to' and sum their flows
    for i in range(len(graph.edges)):
        edge = graph.get_edge(i)
        if edge.v == to:
            flow += edge.flow

    return flow


if __name__ == '__main__':
    graph = read_data()
    print(max_flow(graph, 0, graph.size() - 1))
