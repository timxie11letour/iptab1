#coding=utf-8
'''
Created on 2014-10-14

@author: Liangkangzhu
'''

import commands
import controller

'''
系统信息
'''
class JobExecuter():
    def __init__(self):
        self.agent_config = controller.load_agent_config()
        self.base_path = self.agent_config.get('base_path') + '/resource/temp/job'
    
    '''
    执行指定命令，获取结果
    '''
    def get_command_result_list(self, _command):
        result = commands.getoutput(_command)
        return result
    
    def run(self, _list):
        temp_config_file_path = '{0}/save_job.cfg'.format(self.base_path)
        self.save_config(temp_config_file_path)
        flag = True
        for _dict in _list:
            _dict['executeresult'] = self.get_command_result_list(_dict.get('executecmd'))
            if _dict['executeresult'] == '':
                _dict['executeflag'] = 'true'
            else:
                _dict['executeflag'] = 'false'
                flag = False
        if not flag :
            self.restore_config(temp_config_file_path)
        else:
            #任务执行成功后，重新生成配置文件
            controller.load_config(True)
        return _list
    
    def save_config(self, file_path):
        cmd = 'iptables-save >{0}'.format(file_path)
        commands.getoutput(cmd)
    
    def restore_config(self, file_path):
        cmd = 'iptables-restore <{0}'.format(file_path)
        commands.getoutput(cmd)
    
    
if __name__ == "__main__":
    print JobExecuter()
        
