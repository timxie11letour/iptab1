#coding=utf-8

'''
Created on 2012-9-13

@author: Huiyugeng
'''
import ip, port, protocol
import datetime

'''
策略冗余/冲突分析
@param policy_dict: 分组后的策略集
@param deny_ignore: 是否忽略deny类型策略的分析

@return: 策略冗余/冲突列表
'''
def analyse_policy_compare(src_policy_group, dst_policy_group = None ,deny_ignore = True):
    analysis_policy_list = []
    
    issue_id = 1
    
    for policy_group_name in src_policy_group.keys():
        src_policy_list = src_policy_group[policy_group_name]
        src_policy_len = len(src_policy_list)
        
        for i in range(src_policy_len):
            #通过关键字对源策略进行过滤
            src_policy, key = filter_policy(src_policy_list[i])
            if src_policy == None and key != None:
                continue
            
            #如果匹配的目标策略组存在，则与目标策略组中对应的策略组进行匹配
            if dst_policy_group == None:
                dst_policy_list = src_policy_list[i + 1: src_policy_len]
            else:
                dst_policy_list = dst_policy_group.get(policy_group_name, [])
                
            for dst_policy in dst_policy_list:

                #通过关键字对目的策略进行过滤
                dst_policy, key = filter_policy(dst_policy)
                if dst_policy == None and key != None:
                    continue
                
                #忽略对Deny的分析，源地址和目的地址都为deny的时候才忽略，否则可以进行冲突判断
                if deny_ignore == True and (src_policy.get('action') == 'deny' and dst_policy.get('action') == 'deny'):
                    continue
                
                #跟策略各个项目进行比较
                proto = protocol.compare_protocol_range(src_policy['protocol'], dst_policy['protocol'])
                action = src_policy['action'] == dst_policy['action']
                src_ip = ip.compare_ip_range(src_policy['src-address'], dst_policy['src-address'])
                dst_ip = ip.compare_ip_range(src_policy['dst-address'], dst_policy['dst-address'])
                src_port = port.compare_port_range(src_policy['src-port'], dst_policy['src-port'])
                dst_port = port.compare_port_range(src_policy['dst-port'], dst_policy['dst-port'])
                
                issue = 0 #0:没有发现问题;1:完全冗余;2:交叉冗余;3:冲突
                
                if action == True:
                    if (proto == 1 or proto == 0) and (src_ip == 1 or src_ip == 0) and (dst_ip == 1 or dst_ip == 0) and (src_port == 1 or src_port == 0) and (dst_port == 1 or dst_port == 0):
                        issue = 1
                    #目的策略包含源策略,则为完全冗余
                    elif (proto == 2 or proto == 0) and (src_ip == 2 or src_ip == 0) and (dst_ip == 2 or dst_ip == 0) and (src_port == 2 or src_port == 0) and (dst_port == 2 or dst_port == 0):
                        issue = 1
                    #如果策略全部不同,则为策略不一致,没有策略问题
                    elif proto == -1 or src_ip == -1 or dst_ip == -1 or src_port == -1 or dst_port == -1:
                        issue = 0
                    #其他问题则为交叉冗余
                    else:
                        issue = 2
                        
                elif action == False:
                    #冲突的情况应该是后策略是前策略的子集,但是行为不一样导致
                    if proto == 0 and src_ip == 0 and dst_ip == 0 and src_port == 0 and dst_port == 0:
                        issue = 3

                    elif (proto == 1 or proto == 0) and (src_ip == 1 or src_ip == 0) and (dst_ip == 1 or dst_ip == 0) and (src_port == 1 or src_port == 0) and (dst_port == 1 or dst_port == 0):
                        #获取策略顺序
                        src_policy_id = int(src_policy.get('id')) if src_policy.has_key('id') else 0
                        dst_policy_id = int(dst_policy.get('id')) if dst_policy.has_key('id') else 0
                        
                        #如果后策略为前策略的子集,且协议不一致可判断,后策略与前策略冲突
                        if src_policy_id < dst_policy_id:
                            issue = 3
                            
                    elif (proto == 2 or proto == 0) and (src_ip == 2 or src_ip == 0) and (dst_ip == 2 or dst_ip == 0) and (src_port == 2 or src_port == 0) and (dst_port == 2 or dst_port == 0):
                        #获取策略顺序
                        src_policy_id = int(src_policy.get('id')) if src_policy.has_key('id') else 0
                        dst_policy_id = int(dst_policy.get('id')) if dst_policy.has_key('id') else 0
                        
                        #如果前策略为后策略的子集,且协议不一致可判断,前策略与后策略冲突
                        if src_policy_id > dst_policy_id:
                            issue = 3
                        
                if issue != 0:
                    analysis_policy = {}
                    
                    analysis_policy['id'] = issue_id
                    
                    analysis_policy['src-policy-id'] = src_policy.get('id')
                    analysis_policy['src-policy-group'] = policy_group_name
                    analysis_policy['src-policy'] = src_policy.get('origin-policy')
                    analysis_policy['src-policy-md5'] = src_policy.get('policy-md5')
                    
                    analysis_policy['dst-policy-id'] = dst_policy.get('id')
                    analysis_policy['dst-policy-group'] = policy_group_name
                    analysis_policy['dst-policy'] = dst_policy.get('origin-policy')
                    analysis_policy['dst-policy-md5'] = dst_policy.get('policy-md5')
                    
                    analysis_policy['issue'] = {
                                                1:lambda :'Fully Redundant',
                                                2:lambda :'Cross Redundant',
                                                3:lambda :'Conflict',
                                                }[issue]()
                                                
                    analysis_policy_list.append(analysis_policy)
                    
                    issue_id = issue_id + 1
                    
    return analysis_policy_list

'''
策略范围分析

@param policy_dict: 分组后的策略集
@param deny_ignore: 是否忽略deny类型策略的分析

@return: 范围过宽的策略列表
'''
def analyse_policy_scope(policy_group, deny_ignore=True):
    analysis_policy_list = []
    
    for group_name in policy_group.keys():
        policy_list = policy_group[group_name]
        for policy in policy_list:
            address_list = []
            
            #通过关键字对策略进行过滤
            policy, key = filter_policy(policy)
            if policy == None and key != None:
                continue
            
            #忽略对Deny的分析
            if deny_ignore == True and (policy.get('action') == None or policy.get('action') == 'deny'):
                continue
            
            #策略地址宽松度检查 仅对目的地址进行范围过宽分析
            dst_address_list = policy.get('dst-address').split(',')
            
            #仅对目的地址进行分析
            address_list.extend(dst_address_list)
            
            for address in address_list:
                if '/' in address:
                    ip_address, mask = address.split('/')
                    measure = ip.measure_ip(mask)
                    
                    if measure >= 16: #目前设置宽泛为度为16（B级地址）的就是策略过宽，
                        analysis_policy = {}
                        analysis_policy['src-policy-id'] = policy.get('id')
                        analysis_policy['src-policy-group'] = group_name
                        analysis_policy['src-policy'] = policy.get('origin-policy')
                        analysis_policy['src-policy-md5'] = policy.get('policy-md5')
                        
                        if measure >= 32:
                            analysis_policy['issue'] = 'Wide Scope-ANY'
                        elif measure >= 24 and measure < 32:
                            analysis_policy['issue'] = 'Wide Scope-Class A'
                        elif measure >= 16 and measure < 24:
                            analysis_policy['issue'] = 'Wide Scope-Class B'   
                        elif measure >= 8 and measure < 16:
                            analysis_policy['issue'] = 'Wide Scope-Class C'
                        elif measure > 0:
                            analysis_policy['issue'] = 'Wide Scope-No Host'
                               
                        analysis_policy_list.append(analysis_policy)
                        
                        break
                    
            #策略目的端口宽松度检查        
            dst_port_list = policy.get('dst-port').split(',')
            
            for dst_port in dst_port_list:
                min_port, max_port = port.conver_port(dst_port)
                measure = port.measure_port(min_port, max_port)
                if measure >= 16:
                    analysis_policy = {}
                    analysis_policy['src-policy-id'] = policy.get('id')
                    analysis_policy['src-policy-group'] = group_name
                    analysis_policy['src-policy'] = policy.get('origin-policy')
                    analysis_policy['src-policy-md5'] = policy.get('policy-md5')
                    
                    analysis_policy['issue'] = 'Wide Scope-Port'
                    
                    analysis_policy_list.append(analysis_policy)
                    
                    break
                    
    return analysis_policy_list

'''                
策略过期分析

@param policy_dict: 分组后的策略集

@return: 过期的策略列表
'''
def anaylse_policy_outdate(policy_group):
    outdate_policy_list = []
    
    for group_name in policy_group.keys():
        policy_list = policy_group[group_name]
        for policy in policy_list:
            if policy.get('time-range') != None:
                time_list = policy['time-range'].split(';')
                for time_dict in time_list:
                    time_item = time_dict.split('/')
                    if time_item != None and len(time_item) == 2:
                        end_time = time_dict.split('/')[1]
                        if end_time == None:
                            continue
                    else:
                        continue
                    
                    time_item = end_time.split('-')
                    policy_time = datetime.datetime(int(time_item[0]), int(time_item[1]), int(time_item[2]),
                                                    int(time_item[3]), int(time_item[4]))
                    
                    now = datetime.datetime.now()
                    if policy_time < now:
                        analysis_policy = {}
                        analysis_policy['src-policy-id'] = policy.get('id')
                        analysis_policy['src-policy-group'] = group_name
                        analysis_policy['src-policy'] = policy.get('origin-policy')
                        analysis_policy['src-policy-md5'] = policy.get('policy-md5')
                        
                        analysis_policy['issue'] = 'Out Date'
                        outdate_policy_list.append(analysis_policy)
                        break
    
    return outdate_policy_list

'''
分析未使用的对象或策略
'''
def anaylse_unused_object(used_object_list, object_group):
    unused_object_list = []
    
    for used_object in used_object_list:
        if object_group.has_key(used_object):
            del object_group[used_object]
    
    object_id = 1
    for unused_object_name in object_group:
        
        unused_object = object_group.get(unused_object_name)
        
        detail = str(unused_object.get('value')).strip()
        if detail == '':
            detail = 'NONE'
        
        analysis_object = {}
        analysis_object['src-policy-id'] = str(object_id)
        analysis_object['src-policy-group'] = unused_object.get('type')
        analysis_object['src-policy'] = 'name:{0}; detail:{1}'.format(unused_object_name,  detail)
        analysis_object['src-policy-md5'] = 'NONE'
        
        object_id = object_id + 1
        
        analysis_object['issue'] = 'Unused Object'
        unused_object_list.append(analysis_object)
    
    return unused_object_list
        
#过滤列表
global_keywords_dict = {'protocol' : ['ospf', 'icmp', 'gre']}

'''
策略过滤器，通过过滤器将含有关键字的策略过滤
@param policy_dict: 策略
@param keywords_dict: 关键字集合

@return: 策略,匹配关键字  
'''
def filter_policy(policy_dict, keywords_dict=global_keywords_dict):
    
    for policy_key in policy_dict:
        
        policy_value = policy_dict.get(policy_key) if policy_dict.has_key(policy_key) else ''
        policy_value = policy_value if policy_value != None else ''
        
        if keywords_dict.has_key(policy_key):
            
            keyword_list = keywords_dict.get(policy_key)
            
            for keyword in keyword_list:
                if keyword in policy_value:
                    return None, policy_key
      
    return policy_dict, None


    
