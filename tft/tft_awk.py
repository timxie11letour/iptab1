#coding=utf-8

'''
Created on 2012-8-15

@author: Huiyugeng
'''

import tft_grep
import types

'''
awk
@param regex: 需要匹配的正则表达式，如果为None或空字符串则忽略
@param target: 需要解析的目标，通常为一个list
@param split: 分隔符
@param column: 需要解析的列数

@return: 解析后的结果

@summary: list= ['1:huyugeng:male', '2:zhuzhu:male'];print awk.awk('', _list, ':', [1]); 
            结果 ['huiyugeng', 'zhuzhu']
'''
def awk(regex, target, split, column):
    _list = __list(target)
    if regex !=None and regex !='':
        _list = tft_grep.grep(regex, _list, 'E', False)
    
    result = []
        
    for text in _list:
        if split in text:
            split_list = text.split(split)
            if column == None:
                result.append(split_list)
            else:
                temp_list = []
                for i in column:
                    temp_list.append(split_list[i])
                result.append(temp_list)
                
    return result
    
def __list(target):
    _list = []
    
    if type(target) == types.ListType:
        _list = target
    elif type(target) == types.StringType:
        _file = open(target , 'r')
        for line in _file.readlines():
            _list.append(line)
    
    return _list
