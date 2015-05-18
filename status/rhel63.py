#coding=utf-8
'''
Created on 2014-9-29

@author: Liangkangzhu
'''

import os

'''
系统状态
'''
class Status():
    def __init__(self):
        self.datas = {'memory':{}, 'cpu':{}}
        self.command_dict = {'TOP-one':'top -b -n 1'}
        
        self.memory_parse_handler_param = {
            'start_key':'Mem:',
            'split_key':',',
            'item_split_key':' '
        }
        self.cpu_parse_handler_param = {
            'start_key':'Cpu(s):',
            'split_key':',',
            'item_split_key':'%'
        }
    
    '''
    执行指定命令，获取结果
    '''
    def get_command_result_list(self, _command):
        execute = os.popen(_command)
        result = execute.readlines()
        return result
    
    '''
    处理状态信息内容
    '''
    def handle_status_content_list(self, content_list):
        for line in content_list:
            line = line.strip()
            if line.startswith(self.memory_parse_handler_param['start_key']):
                self.parse_mem(line)
            elif line.startswith(self.cpu_parse_handler_param['start_key']):
                self.parse_cpu(line)
    
    '''
    解析处理通用方法
    '''
    def parse_handler(self, line, param):
        start_key = param.get('start_key')
        split_key = param.get('split_key')
        item_split_key = param.get('item_split_key')
        _line = line[len(start_key):]
        items = _line.split(split_key)
        _dict = {}
        for item in items:
            item = item.strip()
            v,k = item.split(item_split_key)
            _dict[k.strip()]=v.strip()
        return _dict
    
    '''
    解析内存信息
    '''
    def parse_mem(self, line):
        self.datas['memory'] = self.parse_handler(line, self.memory_parse_handler_param)
        _used = self.datas['memory'].get('used','0').replace('k','')
        _total = self.datas['memory'].get('total','0').replace('k','')
        self.datas['memory']['usedpercent'] = str(round(float(_used)/float(_total)*100,1))
        
    
    '''
    解析CPU信息
    '''
    def parse_cpu(self, line):
        _dict = self.parse_handler(line, self.cpu_parse_handler_param)
        self.datas['cpu']['used'] = _dict.get('us','0.0')
        self.datas['cpu']['usedpercent'] = self.datas['cpu'].get('used','0')
    
    '''
    获取状态信息
    '''
    def get_status_info(self):
        content_list = self.get_command_result_list(self.command_dict['TOP-one'])
        self.handle_status_content_list(content_list)
        return self.datas
    
if __name__ == "__main__":
    line_list = [
                "top - 10:42:11 up 59 min,  3 users,  load average: 0.59, 0.40, 0.23",
                "Tasks: 147 total,   1 running, 146 sleeping,   0 stopped,   0 zombie",
                "Cpu(s):  1.0%us,  1.7%sy,  0.2%ni, 96.9%id,  0.1%wa,  0.0%hi,  0.0%si,  0.0%st",
                "Mem:   2061196k total,  1142204k used,   918992k free,   136744k buffers",
                "Swap:  1340408k total,        0k used,  1340408k free,   560760k cached"
                ]
    ss = Status()
    ss.handle_status_content_list(line_list)
    print ss.datas
    
        