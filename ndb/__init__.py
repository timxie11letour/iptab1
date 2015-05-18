#coding=utf-8

import node_reader
import node_writer
import node_query
import node_filter

def load(filename):
    return node_reader.NodeReader().load(filename)

def load_string(data):
    return node_reader.NodeReader().load_string(data)

def build_node(node_name, node_info):
    return node_writer.NodeWriter().build_node(node_name, node_info)

def build_xml(node_name, node_info):
    return node_writer.NodeWriter().build_xml(node_name, node_info)

def query(query_str, node_info, multi):
    return node_query.NodeQuery().query(query_str, node_info, multi)

def filter_list(table, query=None, union=False, sort_key=None):
    return node_filter.NodeFilter().filter_list(table, query, union, sort_key)