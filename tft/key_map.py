#coding=utf-8

'''
Created on 2012-12-20

@author: huiyugeng
'''

'''
根据关键字解析字符串
例如 service 0 protocol tcp dst-port 80 to 81
定义 service protocol dst-port为关键字
则获得{'service':'0', 'protocol':'tcp', 'dst-port', '80 to 81'}

@param string: 需要解析的字符串
@param split: 字符串分割符
@param keys: 关键字列表

@return: 解析后的字典 
'''
def map_str(string, split, keys):
    result = {}
    if split == None or split == '':
        split = " "
    items = string.split(split)
    key = None
    value = ''
    for item in items:
        if item in keys:
            if value != '' and key != None:
                result[key] = value.strip()
            key = item
            value = ''
        else:
            value = value + ' ' + item
            
    #将最后一个条目加入结果集        
    if key != None and value != None:
        result[key] = value.strip()
    return result
