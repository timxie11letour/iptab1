#coding=utf-8

'''
Created on 2012-8-27

@author: Huiyugeng
'''

import types

'''
对比列表1, 列表2之间不同，并返回列表2不存在的元素（或相同的元素）
@param src_list1: 需要比对的列表1（列表中每个元素均为Directory，否则忽略key1）
@param src_list2: 需要比对的列表2（列表中每个元素均为Directory，否则忽略key2）
@param key1：列表1的比对关键字
@param key2: 列表2的比对关键字
@param same: True 选取列表1和列表2 都拥有的元素，False 选取列表1有，列表2没有的元素

@return: 返回比较结果集  
'''
def compare(src_list1, src_list2, key1, key2, same=False):
    dst_list = []
    
    if type(src_list1) == types.ListType and type(src_list2) == types.ListType:
        
        for src1 in src_list1:
            find = False
            for src2 in src_list2:
                value1, value2 = src1, src2
                
                if type(src1) == types.DictionaryType and key1 != None:
                    value1 = src1[key1]
                else:
                    value1 = src1
                if type(src2) == types.DictionaryType and key2 != None:
                    value2 = src2[key2]
                else:
                    value2 = src2
                    
                if value1 == value2:
                    find = True
                    break
            
            if same == find:
                dst_list.append(src1)
                
    return dst_list

'''
对比列表1, 列表2之间不同，并返回列表1和列表2不存在的元素

@param src_list1: 需要比对的列表1（列表中每个元素均为Directory，否则忽略key1）
@param src_list2: 需要比对的列表2（列表中每个元素均为Directory，否则忽略key2）
@param key1：列表1的比对关键字
@param key2: 列表2的比对关键字

@return: 返回两个列表，返回列表1为列表1有，列表2没有的元素，返回列表2为列表2有，列表1没有的元素
'''
def compare_diff(src_list1, src_list2, key1, key2):
    dst_list1 = compare(src_list1, src_list2, key1, key2)
    dst_list2 = compare(src_list2, src_list1, key2, key1)
    
    return dst_list1, dst_list2
