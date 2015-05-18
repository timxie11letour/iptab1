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
            'infname':r'(\w+):\sflags=\d*<(.*)>\s+mtu\s\d*',
            'ipaddr':r'inet\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+netmask\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+broadcast\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',
            'ether':'ether\s(\S+)\s*txqueuelen\s\d*\s*\((\S+)\)'
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
                _name,_other_params = regex.get_line(self.regex_dict['infname'], line)
                temp_dict = {'name':_name}
                if 'UP' in _other_params:
                    temp_dict['enable']='true'
                else:
                    temp_dict['enable']='false'
            elif regex.check_line(self.regex_dict['ipaddr'], line):
                _ipaddr,_mask,_bcast = regex.get_line(self.regex_dict['ipaddr'], line)
                temp_dict['ipaddr'] = _ipaddr
                temp_dict['bcast'] = _bcast
                temp_dict['mask'] = _mask
                temp_dict['ip'] = '{0}/255.255.255.255'.format(_ipaddr)
            elif regex.check_line(self.regex_dict['ether'], line):
                HWaddr,link_encap = regex.get_line(self.regex_dict['ether'], line)
                temp_dict['linkencap'] = link_encap
                temp_dict['HWaddr'] = HWaddr
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
    line_list = [
        "ens33: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500",
        "inet 192.168.0.32  netmask 255.255.255.0  broadcast 192.168.0.255",
        "inet6 fe80::20c:29ff:fe07:f9d1  prefixlen 64  scopeid 0x20<link>",
        "ether 00:0c:29:07:f9:d1  txqueuelen 1000  (Ethernet)",
        "RX packets 156700  bytes 164882856 (157.2 MiB)",
        "RX errors 0  dropped 0  overruns 0  frame 0",
        "TX packets 70007  bytes 4906567 (4.6 MiB)",
        "TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0",
        "",
        "lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536",
        "inet 127.0.0.1  netmask 255.0.0.0",
        "inet6 ::1  prefixlen 128  scopeid 0x10<host>",
        "loop  txqueuelen 0  (Local Loopback)",
        "RX packets 10  bytes 870 (870.0 B)",
        "RX errors 0  dropped 0  overruns 0  frame 0",
        "TX packets 10  bytes 870 (870.0 B)",
        "TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0"
        ]
    print SysInfo().parse_inf_info(line_list)