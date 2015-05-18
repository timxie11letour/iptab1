#coding=utf-8

import threading

from common import logger

import controller

import config_cache
import collect


config_task_lock = False

'''
配置采集任务
'''
class CollectConfigTask():
    def __init__(self):
        self.agent_config = controller.load_agent_config()
        self.log = logger.Log()
        
    def __execute(self, fun, arg):
        t = threading.Timer(self.interval, fun, arg)
        t.start()
    
    def __task(self, repeat):
        global config_task_lock
        
        if config_task_lock == False:
            config_task_lock = True #任务锁设置为启用
            try:
                self.log.info('HOST AGENT LOAD CONFIG START')
                controller.load_config(True)
                self.log.info('HOST AGENT LOAD CONFIG END')
            except Exception as e:
                print e
            config_task_lock = False #任务锁设置为关闭
            
        else:
            self.log.info('config_task is locked')
        
        #是否重复执行任务
        if repeat:
            self.__execute(self.__task, [repeat])
    
    def run(self, interval, repeat):
        #设置最小循环周期为60秒
        if repeat == True:
            self.interval = interval if interval > 60 and interval != None else 60
        else:
            self.interval = interval
        
        self.__execute(self.__task, [repeat])
        
'''
状态采集任务
'''
class CollectStateTask():
    def __init__(self):
        self.log = logger.Log()
        
    def __execute(self, fun, arg):
        t = threading.Timer(self.interval, fun, arg)
        t.start()
    
    def __task(self):
        agent_config = controller.load_agent_config()
        
        if agent_config == None:
            return
        
        #防火墙状态解析任务
        if agent_config.get('state_job') != None and agent_config.get('state_job') == 'true':
            self.log.info('HOST AGENT LOAD STATUS START')
            collect.collect().get_status()
            self.log.info('HOST AGENT LOAD STATUS END')
            
        self.__execute(self.__task, [])
    
    def run(self, interval):
        #设置基础延迟启动时间（最小值为60秒）
        self.interval = interval if interval > 60 and interval != None else 60
        
        self.__execute(self.__task, [])
            