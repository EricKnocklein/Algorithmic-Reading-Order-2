import json
import networkx as nx

# get nodes and links

article_nodes = json.load(open("article_nodes.txt"))
names_dict = json.load(open("names_dict.txt"))

# make graph

G = nx.DiGraph()

for a_id in article_nodes:
    G.add_node(a_id)

for m_id in article_nodes:
    for l_id in article_nodes[m_id]["links"]:
        G.add_edge(m_id, l_id)

for node in G.nodes:
    if (node, node) in G.edges:
        G.remove_edge(node, node)

# make transpose of the graph

T = G.reverse()

# function to pick best node from the graph, adds it to the order
# returns the indegree of the node added


def get_and_remove_node(graph, order):

    # get and sort the graph's nodes by indegree

    node_indegree = dict(graph.in_degree)
    node_indegree_list = sorted(node_indegree.items(), key=lambda item: item[1])

    # get the node with lowest indegree

    lowest_indegree = node_indegree_list[0][1]

    node_outdegree = dict(graph.out_degree)

    # get all nodes with the same indegree as the best node. These are our candidates
    best_nodes = []
    for art in node_indegree_list:
        if art[1] <= lowest_indegree:
            best_nodes.append(art)

    # get the node with the highest outdegree of the candidates
    best = best_nodes[0]
    for art in best_nodes:
        if node_outdegree[art[0]] > node_outdegree[best[0]]:
            best = art

    # save the chosen node in the order
    order.append(
        (
            best[0],
            article_nodes[best[0]]["name"],
            node_indegree[best[0]]
        )
    )

    # remove the chosen node from graph
    graph.remove_node(best[0])
    return node_indegree[best[0]]


# Apply algorithm to the graph
orig_order = []
orig_cost = 0

while G.number_of_nodes() > 0:
    orig_cost = orig_cost + get_and_remove_node(G, orig_order)

t = open('topoOrderTest.txt', 'w', encoding="utf8")
for art in orig_order:
    t.write(str(art[1]) + "\n")

t.close()


# Apply algorithm to the transpose of the graph
transpose_order = []
transpose_cost = 0

while T.number_of_nodes() > 0:
    transpose_cost = transpose_cost + get_and_remove_node(T, transpose_order)

t = open('topoOrderTestR.txt', 'w', encoding="utf8")
for art in transpose_order:
    t.write(str(art[1]) + "\n")

t.close()
