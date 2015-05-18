#coding=utf-8

'''
Created on 2012-8-15

@author: Huiyugeng
'''
import re
import types

import txtfile

'''
grep功能
@param regex: 正则表达式，
@param target：需要匹配的目标，list或文件名，
@param model： 模式, E为正则表达式模式，N为行数模式（支持负行数），
@param number： 是否显示行数

@return 处理后的行
'''
def grep(regex, target, model, number=False):
    count = 1;
    _list = __list(target)
    
    result = []
    
    if model == 'N':
        _min, _max = __split_region(regex)
    
    if model == 'E': 
        pattern = re.compile(regex)
                
    for text in _list:
        if model == None or model == '' or model == 'S':
            if regex in text:
                result.append(__print(count, text, number))
        elif model == 'N':
            if len(text) > 3: 
                if count >= _min and count <= _max:
                    result.append(__print(count, text, number))
        elif model == 'E':
            match = pattern.match(text)
            if match:
                result.append(__print(count, text, number))
        count = count + 1
    
    return result

'''
判断正则表达式中描述的行数
'''
def __split_region(regex):
    if regex.startswith('[') and regex.endswith(']') and ',' in regex:
        region = regex[1: len(regex) - 1].split(',')
        _min = int(region[0])
        _max = int(region[1])
        return _min, _max

'''
将目标转换为列表
'''        
def __list(target):
    _list = []
    if type(target) == types.ListType:
        _list = target
    elif type(target) == types.StringType:
        _list = txtfile.load_file_as_list(target)
    
    return _list

'''
输出内容
'''
def __print(count, text, number):
    if number:
        return (str(count) + ':' + text.strip())
    else:
        return text.strip()
    
