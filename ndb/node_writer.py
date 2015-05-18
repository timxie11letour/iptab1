#coding=utf-8

'''
Created on 2012-5-26

@author: Huiyugeng
'''

import types

class NodeWriter():
    '''
    Build Dictionary to Node Information
    
    @param node_name: Root node name
    @param node_info: Dictionary Object
    
    @return: Node Information
    '''
    def build_node(self, node_name, node_info):
        
        result = []
        result.append(node_name + '{\n')
        for key in node_info.keys():
            value = node_info[key]
            if type(value) == types.ListType and len(value)!=0:
                for item in value:
                    if type(item) == types.DictionaryType:
                        result.append(self.build_node(key, item))
                    if type(item) == types.StringType:
                        result.append(key + ':' + item + '\n')
                        
            if type(value) == types.DictionaryType and len(value.keys()) != 0:
                result.append(self.build_node(key, value))
                
            if (type(value) == types.StringType or type(value) == types.UnicodeType) and value != '':
                result.append( key + ':' + value +'\n')
            
            if type(value) == types.IntType or type(value) == types.LongType or type(value) == types.BooleanType:
                result.append( key + ':' + str(value) +'\n')
            
        result.append('}\n')
        return ''.join(result)
    
    '''
    Build Dictionary to XML Information
    
    @param node_name: Root node name
    @param node_info: Dictionary Object
    
    @return: XML Information
    '''    
    def build_xml(self, node_name, node_info):
        result = []
        result.append('<' + node_name + ">\n")
        for key in node_info.keys():
            value = node_info[key]
            if type(value) == types.ListType and len(value) != 0:
                for item in value:
                    if type(item) == types.DictionaryType:
                        result.append(self.build_xml(key, item))
                    if type(item) == types.StringType:
                        result.append('<' + key + '>' + item + '</' + key + '>\n')
                        
            if type(value) == types.DictionaryType and len(value.keys()) != 0:
                result.append(self.build_xml(key, value))
                
            if (type(value) == types.StringType or type(value) == types.UnicodeType) and value != '':
                result.append('<' + key + '>' + value + '</' + key + '>\n')
            
        result.append('</' + node_name + ">\n")
        return ''.join(result)
    
    '''
    convert dictionary to string
    '''
    def write(self, struct):
        if type(struct) == types.DictionaryType:
            return str(struct)
            
    '''
    convert string to Dictionary
    '''
    def read(self, string):
        if type(string) == types.StringType:
            return eval(string)
