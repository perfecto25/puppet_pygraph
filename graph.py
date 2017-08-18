#!/usr/bin/env python

# Dora the Explora!

from __future__ import print_function
from dora.dora import *

role_names = []
class_names = []
json_dir = 'servers'
selected_role = 'webserver'
selected_class = 'nagios::common'
graph_format = 'png'


# get all available Puppet Roles and Classes from JSON data
all_puppet_roles = get_all_roles(json_dir)
all_puppet_classes = get_all_classes(json_dir)



generate_graph(json_dir, graph_format, 'role', selected_role)
generate_graph(json_dir, graph_format, 'classes', selected_class)






