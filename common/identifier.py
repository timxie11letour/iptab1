#coding=utf-8
'''
Created on 2014-10-13

@author: Liangkangzhu
'''

import uuid
import hashlib

'''
生成MD5值
'''
def get_md5(_str):
    return hashlib.md5(_str).hexdigest()

'''
生成唯一编号
'''
def get_uuid():
    return get_md5(str(uuid.uuid4()))

