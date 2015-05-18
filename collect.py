#coding=utf-8
'''
Created on 2014-9-24

@author: Liangkangzhu
'''

import os
import time

import rules, status, sysinfo

import controller
import ndb
from common import identifier

class collect(object):
    def __init__(self):
        self.agent_config = controller.load_agent_config()
        self.base_path = self.agent_config.get('base_path') + '/resource'
        self.config_file_format = '{0}/config/{1}.cfg'
        self.status_file_format = '{0}/status/{1}.lst'
    
    '''
    加载规则列表
    '''
    def load_rules(self):
        return rules.get_rules_info()
    
    '''
    加载系统信息
    '''
    def load_sysinfo(self):
        return sysinfo.get_sysinfo_info()
    
    '''
    加载状态信息
    '''
    def load_status(self):
        return status.get_status_info()
    
    '''
    创建系统配置信息文件
    '''
    def create_config_file(self):
        #采集最新数据
        config_dict = {}
        config_dict.update(self.load_sysinfo())
        config_dict.update(self.load_rules())
        config_content = ndb.build_node('config', config_dict)
        self.save_config_file(config_content)
        return config_dict
    
    '''
    保存系统配置信息文件，根据内容MD5判断跟上一次是否重复而确定保存的结果
    '''
    def save_config_file(self, config_content):
        _md5 = identifier.get_md5(config_content)
        if self.agent_config.get('last_version_md5') == _md5:
            return
        update_time = time.strftime('%Y-%m-%d-%H-%M-%S')
        config_file_path = self.config_file_format.format(self.base_path, update_time)
        config_file = open(str(config_file_path), 'w')
        config_file.write(config_content)
        config_file.close()
        controller.update_agent_config('last_version', update_time)
        controller.update_agent_config('last_version_md5', _md5)
    
    '''
    获取系统配置信息
    '''
    def get_config(self, force_refresh=False):
        last_version = self.agent_config.get('last_version', 'none')
        config_file_path = self.config_file_format.format(self.base_path, last_version)
        config_dict = {}
        if not force_refresh and os.path.isfile(config_file_path):
            config_dict = ndb.load(config_file_path)
            config_dict = config_dict.get('config')
            if config_dict == None:
                config_dict = self.create_config_file()
        else:
            config_dict = self.create_config_file()
        return config_dict
    
    '''
    获取状态信息
    '''
    def get_status(self):
        cur_status = self.load_status()
        collect_date = time.strftime('%Y-%m-%d')
        collect_time = time.strftime('%Y-%m-%d-%H-%M-%S')
        status_file_path = self.status_file_format.format(self.base_path, collect_date)
        save_content = '{0}={1}\n'.format(collect_time,str(cur_status))
        status_file = open(str(status_file_path), 'a')
        status_file.write(save_content)
        status_file.close()
        return cur_status
    
if __name__ == "__main__":
    print collect().get_status()
