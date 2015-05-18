#coding=utf-8

'''
Created on 2014-9-23

@author: Liangkangzhu
'''

import os

import tft

import agent_cache

'''
代理控制器配置文件
'''
class AgentConfig:
    def __init__(self):
        self.config_file = os.path.dirname(__file__) + '/config.fwm'
        
    '''
    载入代理控制器配置文件
    '''
    def load_agent_config(self):
        return agent_cache.load_agent_config(self.config_file)
    
    '''
    保存代理控制器配置文件
    '''
    def save_agent_config(self, config):
        tft.save_property(self.config_file, config)
        agent_cache.load_agent_config(self.config_file, True)
    
    '''
    更新代理控制器配置文件
    '''
    def update_agent_config(self, _key, _value):
        config = self.load_agent_config()
        config[_key] = str(_value)
        self.save_agent_config(config)
    
