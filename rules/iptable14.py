#coding=utf-8
'''
Created on 2014-9-29

@author: Liangkangzhu
'''
import os
import regex
from common import identifier

class Rules():
    def __init__(self):
        self.command_dict = {
            'rule-list':'iptables -nL --line-number',
            'rule-list-ext':'iptables -nvL --line-number'
        }
        self.regex_dict = {
            'chainname':r'Chain\s(\S+)\s.*',
            'start':'num',
            'rule':r'\d.*'
        }
    
    '''
    执行指定命令，获取结果
    '''
    def get_command_result_list(self, _command):
        execute = os.popen(_command)
        result = execute.readlines()
        return result
    
    '''
    解析规则列表
    '''
    def parse_rules_list(self, _list):
        rules_group = []
        rules_list = []
        temp_group_name = None
        for line in _list:
            line = line.strip()
            #跳过列表栏
            if self.regex_dict['start'] in line:
                continue
            if regex.check_line(self.regex_dict['chainname'], line):
                _name = regex.get_line(self.regex_dict['chainname'], line)[0]
                rules_group.append({'name':_name,'enable':'true'})
                temp_group_name = _name
            elif regex.check_line(self.regex_dict['rule'], line):
                rule_item_list = regex.split('\s+', line)
                _ruleid = rule_item_list[0]
                _group = temp_group_name
                _action = rule_item_list[1]
                if _action == 'ACCEPT':
                    _action = 'permit'
                elif _action == 'DROP':
                    _action = 'deny'
                _protocol = rule_item_list[2]
                _srcaddress = rule_item_list[4]
                if _srcaddress != None and _srcaddress != '' and '/' not in _srcaddress :
                    _srcaddress = _srcaddress + '/32'
                _dstaddress = rule_item_list[5]
                if _dstaddress != None and _dstaddress != '' and '/' not in _dstaddress :
                    _dstaddress = _dstaddress + '/32'
                _srcport = ''
                _dstport = ''
                if len(rule_item_list) == 8:
                    _type, _value = self.parse_rule_port(rule_item_list[7])
                    if _type == 'srcport':
                        _srcport = _value
                    elif _type == 'dstport':
                        _dstport = _value
                if len(rule_item_list) == 9:
                    _type_1, _value_1 = self.parse_rule_port(rule_item_list[7])
                    if _type_1 == 'srcport':
                        _srcport = _value_1
                    elif _type_1 == 'dstport':
                        _dstport = _value_1
                    _type_2, _value_2 = self.parse_rule_port(rule_item_list[8])
                    if _type_2 == 'srcport':
                        _srcport = _value_2
                    elif _type_2 == 'dstport':
                        _dstport = _value_2
                _md5 = self.get_md5_value(_group,_protocol,_srcaddress,_dstaddress,_srcport,_dstport,_action)
                rule_dict = {'ruleid':_ruleid,'group':_group,'protocol':_protocol,'srcaddress':_srcaddress,'dstaddress':_dstaddress,'srcport':_srcport,'dstport':_dstport,'action':_action,'md5':_md5}
                rules_list.append(rule_dict)
        
        return {'rulegroups':rules_group,'rules':rules_list}
    
    '''
    解析规则端口
    '''  
    def parse_rule_port(self, _item):
        _items = _item.split(':')
        if _items[0] == 'spt':
            return 'srcport',_items[1]
        elif _items[0] == 'dpt':
            return 'dstport',_items[1]
        elif _items[0] == 'spts':
            return 'srcport','{0}:{1}'.format(_items[1], _items[2])
        elif _items[0] == 'dpts':
            return 'dstport','{0}:{1}'.format(_items[1], _items[2])
        return '',''
    
    '''
    根据五元组获取MD5的值
    '''
    def get_md5_value(self,group,protocol,srcaddress,dstaddress,srcport,dstport,action):
        return identifier.get_md5('{0}-{1}-{2}-{3}-{4}-{5}-{6}'.format(group,protocol,srcaddress,dstaddress,srcport,dstport,action))
    
    '''
    获取规则信息
    '''
    def get_rules_info(self):
        command_result_list = self.get_command_result_list(self.command_dict['rule-list'])
        result_dict = self.parse_rules_list(command_result_list)
        return result_dict
    
    
if __name__ == "__main__":
    print Rules().get_rules_info()