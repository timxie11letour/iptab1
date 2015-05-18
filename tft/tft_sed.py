#coding=utf-8

'''
Created on 2012-8-15

@author: Huiyugeng
'''

import re
import types

import txtfile
'''
sed
@param regex: 需要匹配的正则表达式，如果为None或空字符串则忽略
@param model: 匹配模式 
@param replace:被替换的字符串
@param target: 需要解析的目标，通常为一个list或者一个文件
@param operate: 操作符, D:删除, R:替代
@prarm output: 输出模式 RL:返回列表形式的处理结果, RT:返回文本形式的处理结果, P:屏幕打印, W:写入文件(target需要为文件)

@return: 处理后的结果
'''
def sed(regex, model, replace, target, operate, output):
    _list = __list(target)
    result = []
    
    pattern = re.compile(regex)
    for text in _list:
        match = False
        
        if model == 'E':
            match = pattern.match(text)
        elif model == 'S':
            match = regex in text
            
        if match:
            if operate == 'R':
                result.append(replace)
        else:
            result.append(text)
                
    output_result = ''.join(result)
    
    if output == 'P':
        print output_result
    elif output == 'W':
        if type(target) == types.StringType:
            _file = open(target, 'w')
            _file.write(output_result)
            _file.close()
    elif output == 'RL':
        return _list
    elif output == 'RT':
        return output_result


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
    