#coding=utf-8

'''
Created on 2014-9-23

@author: Liangkangzhu
'''

import copy
import tft

#代理配置信息缓存
agent_config_cache = {}

'''
载入代理配置信息
'''
def load_agent_config(config_file, force_refresh=False):
    global agent_config_cache
    
    if len(agent_config_cache) == 0 or force_refresh:
        agent_config_cache = tft.load_property(config_file)
    
    return copy.deepcopy(agent_config_cache)

