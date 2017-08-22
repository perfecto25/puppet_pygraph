#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import glob
import json
import pydot
from collections import OrderedDict

#---------------------------------------------------------------------------
def get_node_color(env):
    ''' get color of each node according to environment '''
    if env == 'prod':
        node_color = '#e24d4d'
    elif env == 'eu':
        node_color = 'grey'
    elif env == 'dmz':
        node_color = '#cc99ff'
    elif env == 'bidstrading':
        node_color = '#c4ffaa'
    elif env == 'test':
        node_color = '#66ffff'
    elif env == 'dr':
        node_color = '#e0d323'
    elif env == 'drdmz':
        node_color = '#fff799'
    else:
        node_color = '#f7b722'
    return node_color

#---------------------------------------------------------------------------
def get_all_roles(json_dir):
    ''' get a List of all Puppet Roles scrubbed from json files '''

    all_roles = []
    # get all Roles and Classes - turn this into function
    for filename in glob.glob(json_dir+'/*'):
        with open(filename) as json_data:
            try:
                data = json.load(json_data)
            except ValueError, e:
                print('Decoding JSON has failed: %s' % filename)
                print(e)

            try:
                role = data['role']
                all_roles.append(role)
            except KeyError:
                continue
            return list(set(all_roles))

#---------------------------------------------------------------------------
def get_all_classes(json_dir):
    ''' get a List of all Puppet classes scrubbed from json files '''

    for filename in glob.glob(json_dir+'/*'):
        with open(filename) as json_data:
            data = json.load(json_data)
            all_classes = []
            try:
                class_ = data['classes']
                for cls in class_:
                    all_classes.append(cls)
            except KeyError:
                continue
            return list(set(all_classes))

#---------------------------------------------------------------------------
def get_hostname(name):
    ''' gets the shortname for a server from a long filename '''
    return name.split('/')[-1].split('.')[0]

#---------------------------------------------------------------------------
def get_environment(name):
    ''' gets environment from path name '''
    return name.split('/')[-1].split('.')[1] 

#---------------------------------------------------------------------------
def generate_graph_role_class(json_dir, graph_format, sel_type, sel_value):
    '''
    creates a graph of a selected Puppet Role or Class with all attached/related hostnames
    Usage: generate_graph('/tmp/my_jsons', 'png', 'role', 'webserver')
    '''
    #hosts_hash = {}
    env_hash = {} # hash of environments
    host_list = [] # array of hostname+env

    node_count = 0  # total # of nodes in graph

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

            # if hostname json matches selected Role, add to host_list
            if sel_value in search_val:
                if not env in env_hash:
                    env_hash[env] = []
                env_hash[env].append(hostname)

                

            # arrange all hostames alphabetically for each ENV 
            for key in env_hash:
                env_hash[key].sort()
    #print(host_list)
    # now graph it
    graph = pydot.Dot(graph_type='graph', 
                      label='Puppet %s: %s' % (sel_type.title(), sel_value), 
                      labelloc='top',
                      fontsize=20,
                      labelfontname='serif',
                      labelfontcolor='blue',
                      width=1,
                      orientation='portrait',
                      #concentrate='true',
                      #size="1,3",
                      #fontname="serif",
                      page='1',
                     # lwidth='1', # del
                      rankdir='LR', 
                     # graph_layout='shell', 
                      #pad=".2"
                      )

    primary_node = pydot.Node("%s" % '"{0}"'.format(sel_value), 
                              fontname="serif",
                              fontsize=15,
                              style='filled', 
                              shape='oval', 
                              fillcolor='white'
                              )

    #graph.add_node(primary_node)

    for env in env_hash:
        node_color = get_node_color(env)
        for hostname in env_hash[env]:
            # add to flat Hostname list
            host_list.append(hostname+'.'+env)

            child_node = pydot.Node("%s" % hostname+'.'+env, 
                                    style="filled", 
                                    shape='box', 
                                    fontname='Arial',
                                    #rank='same',
                                    fontsize=10, 
                                    fillcolor=node_color, 
                                    margin=0)
            graph.add_node(child_node)
            #graph.add_edge(pydot.Edge(primary_node, child_node, color="#999999", style="invis"))

            # add invisible edge to opposite node, create circle
            curr_index = host_list.index(hostname+'.'+env)
            if env in host_list[curr_index - 1]:
                graph.add_edge(pydot.Edge(child_node, host_list[curr_index - 1], style="line"))
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
    print(host_list)
    # available graphviz engines:
    # circo, dot, fdp, neato, osage, sfdp, twopi, Tools
    graph.write_png('images/'+sel_value+'.png', prog='dot')
