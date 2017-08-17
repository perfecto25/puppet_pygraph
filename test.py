#!/usr/bin/env python

import pydot
import graphviz

graph = pydot.Dot(graph_type='graph')

node_a = pydot.Node("Node A", style="filled", fillcolor="red")
node_b = pydot.Node("Node B", style="filled", fillcolor="green")
node_c = pydot.Node("Node C", style="filled", fillcolor="#0000ff")
node_d = pydot.Node("Node D", style="filled", fillcolor="#976856")

graph.add_node(node_a)
graph.add_node(node_b)
graph.add_node(node_c)
graph.add_node(node_d)

graph.add_edge(pydot.Edge(node_a, node_b))
graph.add_edge(pydot.Edge(node_b, node_c))
graph.add_edge(pydot.Edge(node_c, node_d))

edge = pydot.Edge(node_d, node_a)
edge.set_label("and back we go again")
edge.set_labelfontcolor("#009933")
edge.set_fontsize("10.0")
edge.set_color("blue")
graph.add_edge(edge)

# for i in range(4):
#     edge = pydot.Edge("king", "lord%d" % i)
#     graph.add_edge(edge)

# vassal_num = 0
# for i in range(4):
#     for j in range(7):
#         edge = pydot.Edge("lord%d" % i, "vassal%d" % vassal_num)
#         graph.add_edge(edge)
#         vassal_num = vassal_num + 1

#graph.write_png('example1_graph.svg')
#graph.write_svg('test.svg')
string = graph.create_svg()
print string