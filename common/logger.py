#coding=utf-8

'''
Created on 2012-6-30

@author: Huiyugeng
'''

import logging.config
import os

logger = None

'''
日志处理
'''
class Log():
    def __init__(self):
        if logger == None:
            global logger
            logging.config.fileConfig(os.path.dirname(__file__) + '/logging.conf')
            logger = logging.getLogger('root')

    def debug(self, msg):  
        if msg is not None:  
            logger.debug(msg)  
    def info(self, msg):  
        if msg is not None:  
            logger.info(msg)  
    def warning(self, msg):  
        if msg is not None:  
            logger.warning(msg)  
    def error(self, msg):  
        if msg is not None:  
            logger.error(msg)  
    def critical(self, msg):  
        if msg is not None:  
            logger.critical(msg) 
