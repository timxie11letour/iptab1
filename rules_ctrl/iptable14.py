#coding=utf-8
'''
Created on 2014-9-29

@author: Liangkangzhu
'''

class Rule():
    def __init__(self):
        pass
    
    def bulid_create_cmd(self, _dict):
        cmd_list = []
        cmd_list.append('-A {0}'.format(_dict.get('group')))
        cmd_list.append(self.append_five_tuple(_dict))
        return ' '.join(cmd_list)
    
    def bulid_insert_cmd(self, _dict):
        cmd_list = []
        _insert_str = '-I {0}'.format(_dict.get('group'))
        _ruleid = _dict.get('ruleid')
        if _ruleid != None and _ruleid.strip() != '':
            _insert_str = '{0} {1}'.format(_insert_str, _ruleid)
        cmd_list.append(_insert_str)
        cmd_list.append(self.append_five_tuple(_dict))
        return ' '.join(cmd_list)
    
    def bulid_delete_cmd(self, _dict):
        cmd_list = []
        cmd_list.append('-D {0} {1}'.format(_dict.get('group'), _dict.get('ruleid')))
        return ' '.join(cmd_list)
    
    def bulid_update_cmd(self, _dict):
        cmd_list = []
        cmd_list.append('-R {0} {1}'.format(_dict.get('group'), _dict.get('ruleid')))
        cmd_list.append(self.append_five_tuple(_dict))
        return ' '.join(cmd_list)
        
    def append_five_tuple(self, _dict):
        cmd_list = []
        #针对create和insert追加的
        if _dict.get('operate') in ['create', 'insert', 'update']:
            #源地址
            cmd_list.append('-s {0}'.format(_dict.get('srcaddress')))
            #目的地址
            cmd_list.append('-d {0}'.format(_dict.get('dstaddress')))
            #协议
            _protocol = _dict.get('protocol')
            if _protocol != None and _protocol.strip() != '':
                cmd_list.append('-p {0} -m {0}'.format(_protocol))
                #源端口
                if '!' in _dict.get('srcport'):
                    cmd_list.append('! --sport {0}'.format(_dict.get('srcport').replace('!','')))
                else:
                    cmd_list.append('--sport {0}'.format(_dict.get('srcport')))
                #目的端口
                if '!' in _dict.get('dstport'):
                    cmd_list.append('! --dport {0}'.format(_dict.get('dstport').replace('!','')))
                else:
                    cmd_list.append('--dport {0}'.format(_dict.get('dstport')))
            #动作
            cmd_list.append('-j {0}'.format(_dict.get('action')))
        return ' '.join(cmd_list)
            
    def check_and_convert_cmd_dict(self, _dict):
        _group = _dict.get('group') 
        _operate = _dict.get('operate')
        _ruleid = _dict.get('ruleid')
        _protocol = _dict.get('protocol')
        _srcaddress = _dict.get('srcaddress')
        _srcport = _dict.get('srcport')
        _dstaddress = _dict.get('dstaddress')
        _dstport = _dict.get('dstport')
        _action = _dict.get('action','ACCEPT')
        if _action == 'permit':
            _action = 'ACCEPT'
        elif _action == 'deny':
            _action = 'DROP'
        _dict['action'] = _action
        return True
    
    def bulid_cmd(self, _dict):
        
        self.check_and_convert_cmd_dict(_dict)
        
        cmd_list = ['iptables']
        #操作类型
        if _dict.get('operate') == 'create':
            cmd_list.append(self.bulid_create_cmd(_dict))
        elif _dict.get('operate') == 'insert':
            cmd_list.append(self.bulid_insert_cmd(_dict))
        elif _dict.get('operate') == 'delete':
            cmd_list.append(self.bulid_delete_cmd(_dict))
        elif _dict.get('operate') == 'update':
            cmd_list.append(self.bulid_update_cmd(_dict))
        
        _dict['executecmd'] = ' '.join(cmd_list)
        
        return _dict['executecmd']
        
    def bulid_cmd_by_list(self, _list):
        for _dict in _list:
            self.bulid_cmd(_dict)
        return _list
