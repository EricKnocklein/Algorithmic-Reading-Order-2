import json
import networkx as nx
from pyvis.network import Network

article_nodes = json.load(open("article_nodes.txt"))
names_dict = json.load(open("names_dict.txt"))

G = nx.DiGraph()

for a_id in article_nodes:
    G.add_node(a_id)

for m_id in article_nodes:
    for l_id in article_nodes[m_id]["links"]:
        G.add_edge(m_id, l_id)

for node in G.nodes:
    if (node, node) in G.edges:
        G.remove_edge(node, node)

nx.set_node_attributes(G, names_dict, 'label')
net = Network(width="1080px", height="840px", bgcolor="#333333ff", font_color="white", directed=True)
net.from_nx(G)
net.show_buttons(filter_=['physics'])
net.show("graph.html")
