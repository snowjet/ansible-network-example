#!/usr/bin/env python3
import os
import argparse 
from pathlib import Path
from graphviz import Digraph

ROUTER = ''
edges = {}
nodes = {}

import argparse

parser = argparse.ArgumentParser(description='Generate Network Diagram')
parser.add_argument("--git_folder", default="/tmp/router-confs")
args, unknown_args = parser.parse_known_args()


def build_nodes():
  pathlist = Path(args.git_folder).glob('*/*-interfaces')

  for path in pathlist:

    interfaces = []
    ROUTER = str(path).split('/')[-1].replace('-interfaces','')

    with open(str(path), 'r') as f:
      read_array = f.readlines()
      
      my_array = read_array[0]
      my_array = my_array.replace('[','').replace(']','').replace("'",'').split('\\x1bm,')

      del my_array[0:3]
      my_array = my_array[:-1]

      for line in my_array:
        line = line.strip()
        line = line.split(' ')
        line = list(filter(('').__ne__, line))

        if str(line[0]).startswith(('eth','lo')):
          interfaces.append(str(line[0]))
        
        nodes[ROUTER] = "{ " + ROUTER 

        for idx, line in enumerate(interfaces, start=1):
          if idx == 1:
            nodes[ROUTER] =  nodes[ROUTER] + "|{<" + line + "> " + line
          else:
            nodes[ROUTER] =  nodes[ROUTER] + "|<" + line + "> " + line

        nodes[ROUTER] =  nodes[ROUTER] + "}}"

        print(nodes[ROUTER])


def build_edges():
  pathlist = Path(args.git_folder).glob('*/*-neighbors')
  for path in pathlist:

    ROUTER = str(path).split('/')[-1].replace('-neighbors','')

    with open(str(path), 'r') as f:
      read_array = f.readlines()
      
      my_array = read_array[0]
      my_array = my_array.replace('[','').replace(']','').replace("'",'').split('\\x1bm,')

      del my_array[0:5]
      my_array = my_array[:-1]

      for line in my_array:
        line = line.strip()
        line = line.split(' ')
        line = list(map(lambda x: x.replace('\x1b[m',''),line))
        line = list(filter(('').__ne__, line))

        neighbor = str(line[0])
        local_interface = str(line[1])
        neighbor_interface = str(line[-1])

        source = "%s:%s" %(ROUTER, local_interface)
        dest = "%s:%s" %(neighbor, neighbor_interface)

        edges.update({source : dest})


def generate_graphviz():

  network_diag_file = args.git_folder + "/network_diagram"

  color = 'blue'

  dot = Digraph('Network Diagram', filename=network_diag_file, format='pdf', 
              node_attr={'shape': 'record',  'fontname' : "helvetica"})

  dot.attr(overlap='scale')
  dot.attr(splines='true')
  dot.edge_attr.update(arrowhead='None')

  for key, value in nodes.items():
    dot.node(key, value)

  for key, value in edges.items():
    dot.edge(key, value, color=color)

  dot.render(network_diag_file, view=False)
  # dot.view()

build_edges()
build_nodes()
generate_graphviz()


