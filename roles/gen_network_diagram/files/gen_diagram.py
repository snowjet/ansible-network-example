#!/usr/bin/env python

from graphviz import Digraph

color = 'blue'

dot = Digraph('Network Diagram', filename='network_diag.gv', 
            node_attr={'shape': 'record',  'fontname' : "helvetica"})

dot.attr(overlap='scale')
dot.attr(splines='true')

dot.node('R1', r' {R1|{<eth1> eth1 |<eth2> eth2 |<eth3> eth3 |<eth4> eth4 }}' )
dot.node('R2', r' {R2 |{<eth1> eth1 |<eth2> eth2 |<eth3> eth3 |<eth4> eth4 }}' )
dot.node('Server', r' {Server |{<eth0> eth0 |<eth1> eth1 }}' )
dot.node('Client', r' {Client |{<eth0> eth0 |<eth1> eth1 }}' )
dot.node('Bad', r' {Bad |{<eth0> eth0 |<eth1> eth1 }}' )

dot.edge_attr.update(arrowhead='None')

dot.edge('R1:eth2', 'R2:eth2', color=color)
dot.edge('R2:eth4', 'Bad:eth1', color=color)
dot.edge('R2:eth3', 'Client:eth1', color=color)
dot.edge('R1:eth3', 'Server:eth1', color=color)

dot.view()
