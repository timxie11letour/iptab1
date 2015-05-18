# coding=utf-8

'''
Created on 2012-9-13

@author: Huiyugeng
'''
import os
import types
import math

'''
展开PORT列表

@param port_range: 需要展开的端口列表，以，分割

@return: 分割后的端口列表  
'''
def get_port_list(port_range):
    port_list = []
    if ',' in port_range:
        ports = port_range.split(',')
        for port in ports:
            port_list.append(port)
    else:
        port_list.append(port_range)
    
    return port_list

'''
比较两个端口

@param port1: 端口1
@param port2: 端口2  

@return: -1:两个端口不相等；0：两个端口相等，1：PORT1范围>PORT2范围；2:PORT范围>PORT1范围；3：PORT1与PORT2端口有交集
'''
def compare_port(port1, port2):
    result = -1
    
    port1_min, port1_max = conver_port(port1)
    port2_min, port2_max = conver_port(port2)
    
    try:
        port1_min = int(port1_min); port1_max = int(port1_max)
        port2_min = int(port2_min); port2_max = int(port2_max) 
        
        if port1_min == port2_min and port1_max == port2_max:
            result = 0
        elif port1_min <= port2_min and port1_max >= port2_max:
            result = 1
        elif port1_min >= port2_min and port1_max <= port2_max:
            result = 2
        elif port1_min >= port2_min and port1_min <= port2_max:
            result = 3
        elif port2_min >= port1_min and port2_min <= port1_max:
            result = 3
    except:
        pass
    
    return result

'''
端口范围度量
 例如  65535 测量值为 16

@param min_port: 端口起始号
@param max_port: 端口结束号 

@return: 端口范围度量
'''
def measure_port(min_port, max_port):
    try:
        if type(min_port) == types.StringType and min_port.isdigit():
            min_port = int(min_port)
        if type(max_port) == types.StringType and max_port.isdigit():
            max_port = int(max_port)
    except:
        min_port = 0
        max_port = 65535
    
    measure = 0
    if type(max_port) == types.IntType and type(min_port) == types.IntType:    
        measure = max_port - min_port
        measure = 0 if measure < 0 else measure   
    
    if measure == 0:
        return 0
    else:
        return int(round(math.log(measure, 2)))

'''
端口转换
例如 0-65535转换为 元组(0，65535)

@param  port: 需要转换的端口

@return: 转换后的端口元组 
'''
def conver_port(port):
    port_min = '0'; port_max = '0'
    try:
        if ' ' in port:
            port_min, port_max = port.split(' ')
        else:
            if '-' in port and port.count('-') == 1:
                port_min, port_max = port.split('-')
            else:
                port_max = port_min = port
    except:
        return 0, 0
           
    try:
        port_min = int(port_min)
    except ValueError:
        port_min = get_port_map(port_min)
        
    try:
        port_max = int(port_max)
    except ValueError:
        port_max = get_port_map(port_max)
        
    return port_min, port_max

'''
比较端口范围
@param port_range1: 端口组1
@param port_range2: 端口组2  

@return: -1：不相等；0：端口段相等；1：PORT_RANGE1对PORT_RANGE2有完全包含；2：PORT_RANGE2对PORT_RANGE1有完全包含；3：PORT_RANGE1和PORT_RANGE2有交集
'''
def compare_port_range(port_range1, port_range2):

    port1_list = get_port_list(port_range1)
    port2_list = get_port_list(port_range2)
    
    #逐一对比两个端口列表
    compare_list = []
    for port1 in port1_list:
        compare_port_result = -1
        for port2 in port2_list:
            compare_port_result = compare_port(port1, port2)
            if compare_port_result != -1:
                break
        compare_list.append(compare_port_result)
    
    #compare_list过滤,设置两个端口对比区域着陆点
    landing_point_len = abs(len(port1_list) - len(port2_list))
    _compare_list = []
    for compare_result in compare_list:
        if compare_result == -1 and landing_point_len > 0:
            landing_point_len = landing_point_len - 1
        else:
            _compare_list.append(compare_result)
    compare_list = _compare_list 

    #分析compare_list的值
    diff = False; same = False; contain1 = False; contain2 = False; intersection = False
    for compare_result in compare_list:
        if compare_result == -1:
            diff = True
        elif compare_result == 0:
            same = True
        elif compare_result == 1:
            contain1 = True
        elif compare_result == 2:
            contain2 = True
        elif compare_result == 3:
            intersection = True
    
    #生成分析结果    
    if diff == True and same == False and (contain1 == False or contain2 == False) and intersection == False:
        return -1
    
    result = -1

    if same == True and contain1 == False and contain2 == False and intersection == False:
        result = 0 if diff == False else 3;
    if (contain1 == True or contain2 == True) and intersection == False:
        if contain1 == True and contain2 == True:
            result = 3
        elif contain1 == True:
            result = 1
        elif contain2 == True:
            result = 2
    elif (contain1 == True or contain2 == True) or intersection == True:
        result = 3
        
    return result

# 端口映射列表
port_map_list = []

'''
端口映射说明 
例如 www->80,ftp->21
@param port: 需要转换的端口说明，如www,ftp

@return: 转换后的端口号  
'''
def get_port_map(port):
    if port_map_list == None or len(port_map_list) == 0:
        _file = open(os.path.dirname(__file__) + '/port' , 'r')
        
        for line in _file.readlines():
            line = line.strip()
            items = line.split('|')
            if len(items) == 4:
                port_map_list.append({'key': items[0], 'port': items[1],
                                 'protocol': items[2], 'desc': items[3]})
        _file.close()
                
    for port_map in port_map_list:
        if port_map['key'] == port:
            return port_map['port']
    return port
