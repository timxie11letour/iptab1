#coding=utf-8

'''
Created on 2012-6-30

@author: Huiyugeng
'''

import traceback

'''
异常处理
'''
def trace_back():  
    try:  
        return traceback.format_exc()  
    except:  
        return 
