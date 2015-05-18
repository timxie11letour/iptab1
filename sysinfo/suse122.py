#coding=utf-8
'''
Created on 2014-9-29

@author: Liangkangzhu
'''

import os
import regex

'''
系统信息
'''
class SysInfo():
    def __init__(self):
        self.command_dict={'ifconfig':'export LANG=uc_EN \n ifconfig -a'}
        
        self.regex_dict={
            'infname':r'(\S+)\s+Link encap:(\S+)\s+HWaddr\s(\S+)',
            'ipaddr':r'inet\saddr:(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+Bcast:(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+Mask:(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',
            'infenable':'UP BROADCAST RUNNING MULTICAST',
            'infdisable':'BROADCAST MULTICAST'
        }
    
    '''
    执行指定命令，获取结果
    '''
    def get_command_result_list(self, _command):
        execute = os.popen(_command)
        result = execute.readlines()
        return result
    
    '''
    解析网卡信息
    '''
    def parse_inf_info(self,_list):
        result_list = []
        temp_dict = {}
        for line in _list:
            line = line.strip()
            if regex.check_line(self.regex_dict['infname'], line):
                if len(temp_dict)>0 :
                    result_list.append(temp_dict)
                _name,link_encap,HWaddr = regex.get_line(self.regex_dict['infname'], line)
                temp_dict = {'name':_name,'linkencap':link_encap,'HWaddr':HWaddr}
            elif regex.check_line(self.regex_dict['ipaddr'], line):
                _ipaddr,_bcast,_mask = regex.get_line(self.regex_dict['ipaddr'], line)
                temp_dict['ipaddr'] = _ipaddr
                temp_dict['bcast'] = _bcast
                temp_dict['mask'] = _mask
                temp_dict['ip'] = '{0}/255.255.255.255'.format(_ipaddr)
            elif self.regex_dict['infenable'] in line :
                temp_dict['enable']='true'
            elif self.regex_dict['infdisable'] in line :
                temp_dict['enable']='false'
            elif line=='':
                if len(temp_dict)>0 :
                    result_list.append(temp_dict)
                    temp_dict={}
        return result_list
    
    '''
    获取系统信息
    '''
    def get_sysinfo_info(self):
        sysinfo_dict = {}
        sysinfo_dict['networkcard'] = self.parse_inf_info(self.get_command_result_list(self.command_dict['ifconfig']))
        return sysinfo_dict
    
if __name__ == "__main__":
    print SysInfo().get_sysinfo_info()
    
        