#coding=utf-8

'''
Created on 2014-9-23

@author: Liangkangzhu
'''

import copy

import collect

#代理配置信息缓存
config_cache = None
#主机代理的规则列表缓存
host_rules_cache = None
#主机代理的系统信息缓存
host_sysinfo_cache = None

'''
初始化配置信息
'''
def init_config_cache(force_refresh):
    set_config_cache(collect.collect().get_config(force_refresh))

'''
设置配置信息
'''    
def set_config_cache(_config):
    global config_cache
    global host_rules_cache
    global host_sysinfo_cache
    config_cache = _config
    host_rules_cache = {'rules' : _config.get('rules', [])}
    host_sysinfo_cache = {'rulegroups' : _config.get('rulegroups', []), 'networkcard' : _config.get('networkcard', [])}

'''
载入策略规则信息
'''
def load_rules(force_refresh=False):
    global config_cache
    global host_rules_cache
    
    if config_cache == None or host_rules_cache == None or force_refresh:
        init_config_cache(force_refresh)
    
    return copy.deepcopy(host_rules_cache)

'''
载入主机代理的信息
'''
def load_sysinfo(force_refresh=False):
    global config_cache
    global host_sysinfo_cache
    
    if config_cache == None or host_sysinfo_cache == None or force_refresh:
        init_config_cache(force_refresh)
    
    return copy.deepcopy(host_sysinfo_cache)

