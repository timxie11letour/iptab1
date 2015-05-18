#coding=utf-8
'''
Created on 2014-9-23

@author: Liangkangzhu
'''

import sys

from common import logger

from SocketServer import ThreadingTCPServer, BaseRequestHandler
import threading

from net import socketclient

import controller

import config_cache
import agent_cache
import collect

import task_manage

import ndb

#重新设定系统编码为utf-8
#reload(sys)
#sys.setdefaultencoding('utf-8')

log = logger.Log()

def start_tcp_server():
    class Handler(BaseRequestHandler):
        def handle (self):
            addr = self.request.getpeername()
            log.info('Got a connection from {0}'.format(str(addr)))
            while True:
                data = self.request.recv(socketclient.SOCKET_BUFFER_SIZE).strip()
                if not data:break
                log.info('receive from ({0}):\n{1}'.format(self.client_address, data))
                data_dict = ndb.load_string(data)
                taskinfo = data_dict.get('root')
                
                if taskinfo == None:
                    self.request.send('task command error'.encode('utf8'))
                    return
                
                task_type = taskinfo.get('tasktype')
                _type = taskinfo.get('type')
                task_id = taskinfo.get('taskid')
                
                send_data = {'error':'error'}
                if task_type =='collect' and _type == 'rules':
                    data_dict['datas'] = config_cache.load_rules()
                    send_data = ndb.build_node('root', data_dict)
                elif task_type =='collect' and _type == 'agent':
                    data_dict['datas'] = controller.load_agent_config()
                    send_data = ndb.build_node('root', data_dict)
                elif task_type =='collect' and _type == 'status':
                    data_dict['datas'] = collect.collect().load_status()
                elif task_type =='collect' and _type == 'sysinfo':
                    data_dict['datas'] = config_cache.load_sysinfo()
                elif task_type =='control' and _type == 'rule':
                    datas = taskinfo.get('datas')
                    data_dict['datas'] = task_manage.execute_job(task_id, datas)
                elif task_type =='control' and _type == 'preview':
                    datas = taskinfo.get('datas')
                    data_dict['datas'] = task_manage.preview_job(datas)
                send_data = ndb.build_node('root', data_dict)
                self.request.send(send_data.encode('utf8'))
    
    #获取本地IP
    local_ip = controller.load_agent_config().get('host', '127.0.0.1')
    #获取配置文件中的服务端口
    service_port = int(controller.load_agent_config().get('tcp_server_port', 8888))
    
    print 'start server' + str(local_ip) + ':' + str(service_port)
    
    server = ThreadingTCPServer((local_ip, service_port), Handler)
    server.serve_forever()
    
    #server_thread = threading.Thread(target=server.serve_forever)
    #server_thread.setDaemon(True)
    #server_thread.start()

if __name__ == "__main__":
    logger.Log().info('FIMAS AGENT START')
    #启动TCP服务
    start_tcp_server()