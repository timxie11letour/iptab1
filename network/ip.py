# coding=utf-8

'''
Created on 2012-8-18

@author: Huiyugeng
'''

import types
from common import number
import regex

'''
子网掩码地址转换
例如：
24->11111111111111111111111100000000
32->11111111111111111111111111111111

@param mask: 子网掩码

@return: 转换后的子网掩码 
'''
def convert_mask(mask):
    result = ''
    
    if (type(mask) == types.StringType or type(mask) == types.UnicodeType) and mask.isdigit():
        mask = int(mask)
    elif type(mask) != types.IntType:
        mask = 32
            
    i = 0
    while i < mask:
        result = result + '1'
        i = i + 1
        
    j = 0
    while j < (32 - mask):
        result = result + '0'
        j = j + 1
        
    return result

'''
反码子网掩码转换
例如：
0.0.0.255->255.255.255.0
0->255.255.255.255

@param mask: 子网掩码反码

@return : 转换后的子网掩码
'''
def convert_comp_mask(mask):
    mask = mask.strip()
    
    if not regex.check_line('^\d+\.\d+\.\d+\.\d+$', mask):
        return '255.255.255.255'
    
    bin_mask = ''
    if mask == '0':
        mask = '0.0.0.0'
    comp_mask = convert_ip2bin(mask)
    i = 0
    
    if len(comp_mask) != 32:
        return 0
    
    while i < 32:
        if comp_mask[i] == '0':
            bin_mask = bin_mask + '1'
        elif comp_mask[i] == '1':
            bin_mask = bin_mask + '0'
        i = i + 1
    return convert_bin2ip(bin_mask)

'''
IP地址范围度量
 例如：255.255.255.255 测量值为0，255.255.255.0 测量值为 8 ，255.255.0.0 测量值为16
 255.0.0.0 测量值为24 0.0.0.0 测量值为32
@param mask: IP地址/子网掩码

@return: IP范围度量 
'''
def measure_ip(mask):
    measure = 0
    
    if regex.check_line('^\d+\.\d+\.\d+\.\d+$', mask):
        
        bin_ip = convert_ip2bin(mask)
        i = 0
        
        if len(bin_ip) != 32:
            return 0
        
        while i < 32:
            if bin_ip[i] == '1':
                measure = measure + 1
            i = i + 1
        return 32 - measure
    
    return 0

'''
判断两个iP是否同一个子网

@param ip1: IP1地址
@param mask1: IP1地址的子网掩码
@param ip2: IP2地址
@param mask2: IP2地址的子网掩码

@return: 是否同一子网 True 同一子网 False 不同子网 
'''
def is_same_subnetwork(ip1, mask1, ip2, mask2):
    ip1_bin = convert_ip2bin(ip1)
    mask1_bin = convert_ip2bin(mask1)
    
    ip2_bin = convert_ip2bin(ip2)
    mask2_bin = convert_ip2bin(mask2)
    
    and1_bin = calc_ip_and(ip1_bin, mask1_bin)
    and2_bin = calc_ip_and(ip2_bin, mask2_bin)
            
    if and1_bin == and2_bin:
        return True
    else:
        return False

'''
IP地址转换为二进制
255.255.255.0->11111111111111111111111100000000

@param ip: IP地址 

@return: 二进制描述的IP地址
'''
def convert_ip2bin(ip):
    result = ''
    if regex.check_line('^\d+\.\d+\.\d+\.\d+$', ip):
        ips = ip.split('.')
        for ip_item in ips:
            bin_ip_item = number.dec2bin(ip_item)
            item_length = len(bin_ip_item)
            i = 0
            while i < 8 - item_length:
                bin_ip_item = '0' + bin_ip_item
                i = i + 1
            result = result + bin_ip_item
            
    return result

'''
二进制转换为IP地址
11111111111111111111111100000000->255.255.255.0

@param ip: 二进制描述的IP地址

@return: IP地址 
'''
def convert_bin2ip(ip):
    result = ''
    
    if '.' in ip:
        ip = ip.replace('.', '')
        
    if len(ip) == 32:
        i = 0
        while i < 4: 
            result = result + str(int(ip[i * 8 : (i + 1) * 8], 2)) + '.'
            i = i + 1
    if result.endswith('.'):
        result = result[0 : len(result) - 1]
    return result

'''
比对两个IP的交叉情况

@param ip1: IP1地址
@param mask1: IP1地址的子网掩码
@param ip2: IP2地址
@param mask2: IP2地址的子网掩码

@return:  -1:两个IP不相等；0：两个IP相等，1：IP1范围>IP2范围；2:IP2范围>IP1范围
'''
def compare_ip(ip1, mask1, ip2, mask2):
    mask1 = measure_ip(mask1)
    mask2 = measure_ip(mask2)
    
    ip1_bin = convert_ip2bin(ip1)
    ip2_bin = convert_ip2bin(ip2)
    
    mask_measure = 0
    if mask1 > mask2 :
        mask_measure = mask1
    else:
        mask_measure = mask2
    
    ip1_net_bin = ip1_bin[0: 32 - mask_measure]
    ip2_net_bin = ip2_bin[0: 32 - mask_measure]
    if mask1 == mask2:
        if ip1_net_bin == ip2_net_bin:
            return 0
    else:
        if ip1_net_bin == ip2_net_bin:
            and_bin = calc_ip_and(ip1_bin, ip2_bin)
                    
            if ip1_bin == and_bin:
                return 1
            elif ip2_bin == and_bin:
                return 2
    return -1

'''
展开IP段列表，IP地址间以，分割

@param ip_range: 需要展开的IP地址 

@return: 展开后的IP地址列表
'''
def get_ip_list(ip_range):
    ip_list = []
    if ',' in ip_range:
        ips = ip_range.split(',')
        for ip in ips:
            if '/' in ip:
                ip, mask = ip.split('/')
                ip_list.append({'ip' : ip, 'mask' : mask})
    else:
        if '/' in ip_range:
            ip, mask = ip_range.split('/')
            ip_list.append({'ip' : ip, 'mask' : mask})
    return ip_list
            

'''
比对两个IP地址段

@param ip_range1: IP1地址段
@param ip_range2: IP2地址段
  
@return: -1：没有交集；0：地址段相等；1：IP_RANGE1对IP_RANGE2有完全包含；2：IP_RANGE2对IP_RANGE1有完全包含；3：IP_RANGE1和IP_RANGE2有交集
'''
def compare_ip_range(ip_range1, ip_range2):
    
    
    compare_list = []
    
    ip1_list = get_ip_list(ip_range1)
    ip2_list = get_ip_list(ip_range2)
    
    #逐一对比两个地址列表
    for ip1 in ip1_list:
        compare_ip_result = -1
        for ip2 in ip2_list:
            compare_ip_result = compare_ip(ip1['ip'], ip1['mask'], ip2['ip'], ip2['mask'])
            if compare_ip_result != -1:
                break
        compare_list.append(compare_ip_result)
    
    #compare_list过滤,清理多余的不相等
    diff_len = abs(len(ip1_list) - len(ip2_list))
    _compare_list = []
    for compare_result in compare_list:
        if compare_result == -1 and diff_len > 0:
            diff_len = diff_len - 1
        else:
            _compare_list.append(compare_result)
    compare_list = _compare_list
    
    #分析compare_list的值
    diff = False; same = False; contain1 = False; contain2 = False
    for compare_result in compare_list:
        if compare_result == -1:
            diff = True
        elif compare_result == 0:
            same = True
        elif compare_result == 1:
            contain1 = True
        elif compare_result == 2:
            contain2 = True
    
    #生成分析结果        
    if diff == True and same == False and contain1 == False and contain2 == False:
        return -1
    
    result = -1
    
    if same == True and contain1 == False and contain2 == False:
        result = 0 if diff == False else 3;
    elif contain1 == True or contain2 == True:
        if contain1 == True and contain2 == True:
            result = 3
        elif contain1 == True and contain2 == False:
            result = 1
        elif contain1 == False and contain2 == True:
            result = 2
    elif same == True or (contain1 == True or contain2 == True):
        result = 3
    
    return result
    
'''
对两个IP地址进行与（and）运算

@param ip1: 二进制表示IP1地址
@param ip2: 二进制表示IP2地址

@return: AND运算后的IP地址
'''
def calc_ip_and(ip1, ip2):

    and_bin = ''
    if len(ip1) == 32 and len(ip2) == 32:
        i = 0
        while i < 32:
            and_bin = and_bin + str(int(ip1[i]) & int(ip2[i]))
            i = i + 1
            
    return and_bin
