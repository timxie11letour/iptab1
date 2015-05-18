#coding=utf-8

import job

'''
执行任务
'''
def execute_job(job_id, datas):
    return job.Job().execute_job(job_id, datas)

'''
预览任务指令
'''
def preview_job(datas):
    return job.Job().preview_job(datas)