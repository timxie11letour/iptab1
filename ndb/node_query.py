# coding=utf-8

'''
Created on 2012-6-29

@author: Huiyugeng
'''

import types
import regex


class NodeQuery():
    '''
    Search Node
     
    Search query like: A->B->C:Value
     
    @param query_str: search query
    @param node_info: search node(Dictionary Object) 
    @param multi_value: need multi value: True,return multi value;False,return single value
     
    @return search result
    '''
    def query(self, query_str, node_info, multi):
        
        try:
            query_item = query_str
            sub_query = query_str
        
            if type(node_info) == types.ListType:
                value_list = []
                for item in node_info:
                    temp = self.query(query_str, item, multi)
                    if temp != None:
                        if multi == True:
                            value_list.append(temp)
                        else:
                            return temp
                if len(value_list) > 0:
                    return value_list
            
            elif type(node_info) == types.DictionaryType:
                if '->' in query_str:
                    query_item = query_str[0 : query_str.find('->')]
                    sub_query = query_str[query_str.find('->') + 2 : len(query_str)] #2 is "->"'s length
                    
                if query_item != sub_query:
                    if len(query_item) > 2 and query_item.startswith('/') and query_item.endswith('/'):
                        query_item = query_item[1: len(query_item) - 1]
                        for key in node_info:
                            if regex.check_line(query_item, key):
                                return self.query(sub_query, node_info[key], multi)
                    else:   
                        if query_item in node_info:
                            return self.query(sub_query, node_info[query_item], multi)
                else:
                    if ':' in query_item:
                        items = query_item.split(':')
                        if len(items) == 2:
                            src_value = items[1].strip()
                            dst_value = node_info[items[0]].strip()
                            # regex expression match
                            if len(src_value) > 2 and src_value.startswith('/') and src_value.endswith('/'):
                                regex_str = src_value[1: len(src_value) - 1]
                                if regex.check_line(regex_str, dst_value):
                                    return node_info
                            # value region match
                            if len(src_value) > 3 and src_value.startswith('[') and src_value.endswith(']') and ',' in items[1]:
                                region = src_value[1: len(src_value) - 1].split(',')
                                if len(region) == 2 and type(dst_value) == types.StringType:
                                    _min = int(region[0])
                                    _max = int(region[1])
                                    _value = int(dst_value)
                                    if _value >= _min and _value <= _max:
                                        return node_info
                            # startwith match
                            if src_value.startswith('^'):
                                if dst_value.startswith(src_value[1: len(src_value)]):
                                    return node_info
                            # endswith match
                            if src_value.endswith('$'):
                                if dst_value.endswith(src_value[: len(src_value) - 1]):
                                    return node_info
                            # value match
                            else:
                                if dst_value == src_value:
                                    return node_info
                    else:
                        if query_item in node_info:
                            return node_info[query_item]
        except:
            return None


        
