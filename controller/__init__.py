#coding=utf-8

import agent_config

'''
载入代理控制器配置信息
'''
def load_agent_config():
    return agent_config.AgentConfig().load_agent_config()
'''
保存代理控制器配置信息
'''
def save_agent_config(_config):
    return agent_config.AgentConfig().save_agent_config(_config)

'''
更新代理控制器配置文件
'''
def update_agent_config(_key, _value):
    return agent_config.AgentConfig().update_agent_config(_key, _value)


import agent_manage

'''
加载全局配置文件
'''
def load_config(force_refresh=False):
    return agent_manage.AgentManage().load_config(force_refresh)
