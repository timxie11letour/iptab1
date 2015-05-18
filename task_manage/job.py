#coding=utf-8

'''
Created on 2014-10-15

@author: Liangkangzhu
'''

import time

import controller
import job_executer
import rules_ctrl
import tft

class Job():
    def __init__(self):
        self.agent_config = controller.load_agent_config()
        self.job_list_file = self.agent_config.get('base_path') + '/resource/job/job.lst'
        
    def load_job_list_file(self):
        job_list_dict = tft.load_property(self.job_list_file)
        if job_list_dict == None:
            job_list_dict = {}
        return job_list_dict
        
    def save_job_info(self, job_id, _obj):
        job_list_dict = self.load_job_list_file()
        job_list_dict[job_id] = str(_obj)
        tft.save_property(self.job_list_file, job_list_dict)
        
    def get_job_info(self, job_id):
        job_list_dict = self.load_job_list_file()
        return eval(job_list_dict.get(job_id,'{}'))
    
    def get_job_list(self):
        job_list_dict = self.load_job_list_file()
        job_list = []
        for _key in job_list_dict.keys():
            job_list.append(eval(job_list_dict[_key]))
        return job_list
        
    def execute_job(self, job_id, datas):
        rule_list = datas.get('rule', [])
        rule_list = [rule_list] if isinstance(rule_list, dict) else rule_list
        #rule_list.sort(lambda x, y: cmp(x['operateid'], y['operateid']))
        #构建指令
        for _dict in rule_list:
            rules_ctrl.bulid_cmd(_dict)
        execute_result = job_executer.run(rule_list)
        result_dict = {'jobid':job_id, 'datas':execute_result, 'executetime':time.strftime('%Y-%m-%d %H:%M:%S')}
        self.save_job_info(job_id, result_dict)
        return execute_result
    
    def preview_job(self, datas):
        rule_list = datas.get('rule', [])
        rule_list = [rule_list] if isinstance(rule_list, dict) else rule_list
        for _dict in rule_list:
            rules_ctrl.bulid_cmd(_dict)
        return rule_list
        
if __name__ == "__main__":
    print Job().get_job_info('liangkangzhutest1')
