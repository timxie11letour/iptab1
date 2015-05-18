#coding=utf-8
'''
Created on 2012-10-31

@author: root
'''

import types

class NodeReader():
    def __init__(self):
        self.linenum = 0
        
        
    def load_string(self, data):
        try:
            _list = data.split('\n')
        except:
            _list = []
        return self.__parse(_list)
    
    '''
    Load Node File
    @param filename: Node file name
    
    @return: Node File Result(Dictionary Object)
    '''
    def load(self, filename):
        try:
            _list = [line for line in open(filename, 'r').readlines()]
            self.linenum = 0
        except:
            _list = []
        return self.__parse(_list)
    
    '''
    Parse Dictionary Object
    '''
    def __parse(self, _list):
        node_info ={}

        while self.linenum < len(_list):
            
            line = _list[self.linenum].strip()
    
            self.linenum = self.linenum + 1
            
            if line==None or line=='' or line.startswith('#'):
                continue
            
            if line.endswith('{'):
                node_name = line[0: line.find('{')]
                node_value = self.__parse(_list)
                node = node_info.get(node_name)
                
                if node == None:
                    node_info[node_name] = node_value
                else:
                    node_list = node if type(node) == types.ListType else [node]
                    node_list.append(node_value)
                    node_info[node_name] = node_list
                    
            elif line.endswith('}'):
                return node_info
            
            else:    
                if ':' in line:
                    node_name = line[0: line.find(':')]
                    item_value = line[line.find(':') + 1: len(line)]
                
                node_value = node_info.get(node_name) if node_name != None else None
                
                if node_value != None:
                    node_value_list = node_value if type(node_value) == types.ListType else [node_value]
                    node_value_list.append(item_value)   
                    node_info[node_name] = node_value_list
                else:
                    node_info[node_name] = item_value
        
        return node_info
