# python3

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


class MaxMatching:
    def read_data(self):
        n, m = map(int, input().split())
        adj_matrix = [list(map(int, input().split())) for i in range(n)]
        return adj_matrix

    def write_response(self, matching):
        line = [str(-1 if x == -1 else x + 1) for x in matching]
        print(' '.join(line))

    def find_matching(self, adj_matrix):
        # Replace this code with an algorithm that finds the maximum
        # matching correctly in all cases.
        n = len(adj_matrix)
        m = len(adj_matrix[0])

        #create graph from matrix from n to m
        #all edges will be capacity 1
        graph = FlowGraph(n+m+2)
        #add source node with an edge to every n vertex
        for i in range(n):
            graph.add_edge(0,i+1,1)

        #add entries connecting left vertices to right vertices
        for indi, i in enumerate(adj_matrix):
            for indj, j in enumerate(i):
                if j == 1:
                    #add edge with capacity 1
                    graph.add_edge(indi+1,n+indj+1,1)

        #add entries for right vertices with an edge at the sink vertex
        for i in range(m):
            graph.add_edge(n+i+1,n+m+1,1)

        #execute max flow
        max_flow(graph, 0, graph.size() - 1)

        #find matching 
        matching = [-1] * n
        for i in range(n):
            for edgeID in graph.get_ids(i+1):
                edge = graph.get_edge(edgeID)
                if edge.flow > 0:
                    matching[i] = edge.v -n -1

        return matching

    def solve(self):
        adj_matrix = self.read_data()
        matching = self.find_matching(adj_matrix)
        self.write_response(matching)


class StockCharts:
    def read_data(self):
        n, k = map(int, input().split())
        stock_data = [list(map(int, input().split())) for i in range(n)]
        return stock_data

    def write_response(self, result):
        print(result)

    def min_charts(self, stock_data):
        # Replace this incorrect greedy algorithm with an
        # algorithm that correctly finds the minimum number
        # of charts on which we can put all the stock data
        # without intersections of graphs on one chart.
        n = len(stock_data)
        k = len(stock_data[0])
        charts = []
        for new_stock in stock_data:
            added = False
            for chart in charts:
                fits = True
                for stock in chart:
                    above = all([x > y for x, y in zip(new_stock, stock)])
                    below = all([x < y for x, y in zip(new_stock, stock)])
                    if (not above) and (not below):
                        fits = False
                        break
                if fits:
                    added = True
                    chart.append(new_stock)
                    break
            if not added:
                charts.append([new_stock])
        return len(charts)

    def solve(self):
        stock_data = self.read_data()
        result = self.min_charts(stock_data)
        self.write_response(result)

if __name__ == '__main__':
    stock_charts = StockCharts()
    stock_charts.solve()
