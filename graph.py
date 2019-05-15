import json


class Edge():
    def __init__(self):
        self.edge_list = []
        
    def addAttribute(self, filename, change_type, line_num):
        new_change = {'filename': filename, 'change_type':change_type, 'line_num': line_num}
        self.edge_list.append(new_change)


class Graph():
    """有向图"""

    def __init__(self):
        #adj由v指出的边连接的所有点
        self.adj = {}

    def addEdge(self, v, w, filename, change_type, line_num):
        if v not in self.adj.keys():          
            self.adj[v] = {}
        if w not in self.adj[v].keys():
            self.adj[v][w] = Edge()
        self.adj[v][w].addAttribute(filename, change_type, line_num)
        # print(self.adj[v][w].edge_dict['line_num'])


my_graph = Graph()

with open('E:\\git_repo\\analysis_data\\test.json') as load_f:
    load_dict = json.load(load_f)
# print(load_dict)

edges = load_dict['edge']
for edge in edges:
    for change in edge['change']:
        my_graph.addEdge(edge['from_node'], edge['to_node'], change['filename'], change['type'], change['line_num'])
print(my_graph.adj['c']['d'].edge_list)


# a, b, c, d, e, f, g, h = range(8)
# N = [{'b', 'c', 'd', 'e', 'f'},
#      {'c', 'e'},
#      {'d'},
#      {'e'},
#      {'f'},
#      {'c', 'g', 'h'},
#      {'f', 'h'},
#      {'f', 'g'}]
# print(N[a])