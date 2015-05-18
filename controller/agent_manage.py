#coding=utf-8
'''
Created on 2014-10-24

@author: root
'''

import config_cache

class AgentManage():
    def __init__(self):
        pass
    
    def load_config(self, force_refresh=False):
        return config_cache.init_config_cache(force_refresh)