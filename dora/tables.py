#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import glob
import json
import plotly
import plotly.figure_factory as ff
#import pydot
#import plotly.plotly
#import plotly.figure_factory as ff
#from collections import OrderedDict
from dora import get_node_color, get_hostname, get_environment

#---------------------------------------------------------------------------
def generate_table(json_dir, graph_format, sel_type, sel_value):
    '''
    creates a table of a selected Puppet Role or Class with all attached/related hostnames
    Usage: generate_table('/tmp/my_jsons', 'png', 'role', 'webserver')
    '''
    #hosts_hash = {}
    env_hash = {} # hash of environments
    #host_list = [] # array of hostname+env

    matrix = []
    matrix.append(['ENVIRONMENT', 'HOSTNAME', '', ''])

    for filename in glob.glob(json_dir+'/*'):
        with open(filename) as json_data:
            try:
                data = json.load(json_data)
            except ValueError, e:
                print('Decoding JSON has failed: %s' % filename)
                print(e)

            hostname =  get_hostname(filename)
            env = get_environment(filename)

            # if json search value matches selected value
            try:
                search_val = data[sel_type]
            except KeyError:
                continue

            # # if hostname json matches selected Role, add to host_list
            if sel_value in search_val:
                if not env in env_hash:
                    env_hash[env] = []
                env_hash[env].append(hostname)

                

            # # arrange all hostames alphabetically for each ENV 
            # for key in env_hash:
            #     env_hash[key].sort()
 
    for env in env_hash:
        node_color = get_node_color(env)
        for hostname in env_hash[env]:
            # add to flat Hostname list
            matrix.append(['<div style="background-color:{}">'.format(node_color) + str(env)+'</div>', hostname + '</div>'])

    total_count = len(matrix)
    print(total_count)
    matrix.append(['<b>TOTAL</b>', '<b>' + str(total_count) + '</b>'])

    colorscale = [[0, '#02858e'],[.5, '#f2e5ff'],[1, '#ffffff']]

    # create table HTML

    table = ff.create_table(matrix, colorscale=colorscale, height_constant=20)
    plotly.offline.plot(table, auto_open=False, filename='exports/role.html')

            # child_node = pydot.Node("%s" % hostname+'.'+env, 
            #                         style="filled", 
            #                         shape='box', 
            #                         fontname='Arial',
            #                         #rank='same',
            #                         fontsize=10, 
            #                         fillcolor=node_color, 
            #                         margin=0)
            # graph.add_node(child_node)
            # #graph.add_edge(pydot.Edge(primary_node, child_node, color="#999999", style="invis"))

            # # add invisible edge to opposite node, create circle
            # curr_index = host_list.index(hostname+'.'+env)
            # if env in host_list[curr_index - 1]:
            #     graph.add_edge(pydot.Edge(child_node, host_list[curr_index - 1], style="line"))
            #print('curr index %s' % curr_index)
  #          if curr_index >= midpoint:
   #             opposite_index = curr_index - midpoint

                # add edge to opposite node
    #            graph.add_edge(pydot.Edge(child_node, host_list[opposite_index], style="invis"))

                # add edge to neighbor to create visual space
                #graph.add_edge(pydot.Edge(child_node, host_list[curr_index - 1], style="line"))

               # if not curr_index == host_list.index(host_list[-1]):
                 #   graph.add_edge(pydot.Edge(child_node, host_list[curr_index + 1], style="line"))


                #print('oppos %s' % opposite_index)
                #print(host_list[opposite_index])

            #if opposite_index > len(host_list):
            #    opposite_index = max(host_list)
            #print(host_list)
            #print(curr_index)
            #print(opposite_index)
            #print('===========')
            #print(curr_index)

    # for hostname in hosts_hash:
    
    #     env = hosts_hash[hostname]['env']
    #     # print("%s, %s" % (hostname, env))
    #     node_color = get_node_color(env)
    #     host_node = pydot.Node("%s" % hostname, style="filled", shape='box', fillcolor=node_color)
    #     graph.add_node(host_node)
    #     graph.add_edge(pydot.Edge(primary_node, host_node, color="#999999"))
    # print(host_list)
    # # available graphviz engines:
    # # circo, dot, fdp, neato, osage, sfdp, twopi, Tools
    # graph.write_png('images/'+sel_value+'.png', prog='dot')
