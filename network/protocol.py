#coding=utf-8

'''
Created on 2012-9-14

@author: Huiyugeng
'''
import os
'''
展开协议列表

@param protocol_range: 需要展开的协议列表，以，分割

@return: 分割后的协议列表 
'''
def get_protocol_list(protocol_range):
    protocol_list = []
    if ',' in protocol_range:
        protocols = protocol_range.split(',')
        for protocol in protocols:
            protocol_list.append(protocol)
    else:
        protocol_list.append(protocol_range)
    return protocol_list

'''
比较协议范围

@param protocol_range1: 协议列表1 
@param protocol_range2: 协议列表2

@return: -1：不相等；0：协议段相等；1：PROTOCOL_RANGE1对PROTOCOL_RANGE2有完全包含；2：PROTOCOL_RANGE2对PROTOCOL_RANGE1有完全包含
'''
def compare_protocol_range(protocol_range1, protocol_range2):
    result = -1
    
    compare_list = []
    
    protocol1_list = get_protocol_list(protocol_range1)
    protocol2_list = get_protocol_list(protocol_range2)
    
    for protocol1 in protocol1_list:
        compare_protocol_result = -1
        for protocol2 in protocol2_list:
            compare_protocol_result = compare_protocol(protocol1, protocol2)
            if compare_protocol_result != -1:
                break
        compare_list.append(compare_protocol_result)
    
    #diff 不相等，same 协议段相等, contain1 PROTOCOL_RANGE1对PROTOCOL_RANGE2有完全包含, contain2 PROTOCOL_RANGE2对PROTOCOL_RANGE1有完全包含
    diff = False; same = False; contain1 = False; contain2 = False
    for compare_result in compare_list:
        if compare_result == -1:
            diff = True
        elif compare_result == 0:
            same = True
        elif compare_result == 1:
            contain1 = True
        elif compare_result == 2:
            contain2 = True
            
    if diff == True and same == False and (contain1 == False or contain2 == False):
        result = -1
    elif diff == False and same == True and contain1 == False and contain2 == False:
        result = 0;
    elif diff == False and (contain1 == True or contain2 == True):
        if contain1 == True:
            result = 1
        elif contain2 == True:
            result = 2
        
    return result

'''
对比协议

@param protocol1: 协议1
@param protocol2: 协议2  

@return: -1：不相等；0：相等；1：PROTOCOL1包含PROTOCOL2；2：PROTOCOL2包含PROTOCOL1
'''
def compare_protocol(protocol1, protocol2):
    result = -1
    
    protocol_map1 = get_protocol_map(protocol1)
    protocol_map2 = get_protocol_map(protocol2)
    protocol_layer1 = int(protocol_map1['layer']) if protocol_map1.has_key('layer') else 3
    protocol_layer2 = int(protocol_map2['layer']) if protocol_map2.has_key('layer') else 3
    protocol_ignore1 = protocol_map1['ignore'] if protocol_map1.has_key('ignore') else 'false'
    protocol_ignore2 = protocol_map2['ignore'] if protocol_map2.has_key('ignore') else 'false'
    
    #如果其中一种协议的忽略参数设置为true，仅比较协议名称相同
    if protocol_ignore1 == 'true' or protocol_ignore2 == 'true':
        if protocol1 != protocol2:
            result = -1
        elif protocol1 == protocol2:
            result = 0
        
        return result
    
    #如果协议的忽略参数设置为false，比较协议层和名称
    if protocol_layer1 == protocol_layer2:
        if protocol1 != protocol2:
            result = -1
        elif protocol1 == protocol2:
            result = 0
    elif protocol_layer1 < protocol_layer2:
        result = 1
    elif protocol_layer1 > protocol_layer2:
        result = 2
    
    return result

#协议映射列表    
protocol_map_list = []

'''
协议映射说明
@param protocol: 需要映射的协议 

@return: 协议映射结果，其中layer代表7层模型中第N层协议
'''
def get_protocol_map(protocol):
    if protocol_map_list == None or len(protocol_map_list) == 0:
        _file = open(os.path.dirname(__file__) + '/protocol' , 'r')
        
        for line in _file.readlines():
            if not line.startswith('#'):
                line = line.strip()
                items = line.split('|')
                if len(items) == 3:
                    protocol_map_list.append({'protocol': items[0], 'layer': items[1], 'ignore':items[2]})
                
        _file.close()
    for protocol_map in protocol_map_list:
        if protocol_map['protocol'] == protocol:
            return protocol_map
    return {'protocol': 'ip', 'layer': '3', 'ignore':'false'}
    

    
