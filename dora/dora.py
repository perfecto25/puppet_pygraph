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
    elif env == 'tx':
        node_color = 'grey'
    elif env == 'dmz':
        node_color = '#cc99ff'
    elif env == 'dev':
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
            data = json.load(json_data)

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
def generate_graph(json_dir, graph_format, sel_type, sel_value):
    '''
    creates a graph of a selected Puppet Role or Class with all attached/related hostnames
    Usage: generate_graph('/tmp/my_jsons', 'png', 'role', 'webserver')
    '''
    hosts_hash = {}



    for filename in glob.glob(json_dir+'/*'):
        with open(filename) as json_data:
            data = json.load(json_data)
            hostname =  get_hostname(filename)
            env = get_environment(filename)

            # if json search value matches selected value
            try:
                search_val = data[sel_type]
            except KeyError:
                continue

            # if hostname json matches selected Role, add to host_list
            if sel_value in search_val:
                hosts_hash[hostname] = {'env':env}

    # sort hosts_hash by ENV
    hosts_hash = OrderedDict(sorted(hosts_hash.items(), key=lambda x: x[1]))

    # now graph it
    graph = pydot.Dot(graph_type='graph', graph_name='XXI')
    primary_node = pydot.Node("%s" % '"{0}"'.format(sel_value), style='filled', shape='egg', fillcolor='white')
    graph.add_node(primary_node)

    for hostname in hosts_hash:
        env = hosts_hash[hostname]['env']
        node_color = get_node_color(env)
        host_node = pydot.Node("%s" % hostname, style="filled", shape='box', fillcolor=node_color)
        graph.add_node(host_node)
        graph.add_edge(pydot.Edge(primary_node, host_node, color="#999999"))

    graph.write_png(sel_value+'.png')
