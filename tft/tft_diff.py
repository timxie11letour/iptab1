'''
Created on 2013-2-24

@author: Huiyugeng
'''

import os
import types
import difflib
import txtfile


'''
compare differnet between two file list

@param src_filename: Source Filename List
@param dst_filename: Destination Filename  List

@return: two file list differents
'''
def compare_file_list(src_file_list, dst_file_list, compare_fun):
    changed_list = []
    
    if compare_fun == None:
        compare_fun = diff_text
    
    for src_file in src_file_list:
        src_content = txtfile.load_file_as_list(src_file)
        
        action = 'no-found'
        
        for dst_file in dst_file_list:
            dst_content = txtfile.load_file_as_list(dst_file)
            
            compare_result = compare_fun(src_content, dst_content)
            
            if compare_result.get('action') == 'no-found':
                continue
            else:
                action = compare_result.get('action')
                break
        
        changed_item = {}
        
        if action == 'changed':
            changed_item['src'] = ';'.join([line.strip() for line in src_content])
            changed_item['dst'] = ';'.join([line.strip() for line in dst_content])
            changed_item['action'] = 'changed'
        elif action == 'no-found':
            changed_item['src'] = ';'.join([line.strip() for line in src_content])
            changed_item['action'] = 'delete'
        
        if changed_item.has_key('action'):
            changed_list.append(changed_item)
    
    for dst_file in dst_file_list:
        dst_content = txtfile.load_file_as_list(dst_file)
        
        action = 'no-found'
        
        for src_file in src_file_list:
            src_content = txtfile.load_file_as_list(src_file)
            
            compare_result = compare_fun(src_content, dst_content)
            
            if compare_result.get('action') == 'no-found':
                continue
            else:
                action = 'found'
        
        changed_item = {}
        if action == 'no-found':
            changed_item['dst'] = ';'.join([line.strip() for line in dst_content])
            changed_item['action'] = 'create'
            changed_list.append(changed_item)
            
    return changed_list

'''
compare differnet between two files and split line

@param src_filename: Source Filename or Text List
@param dst_filename: Destination Filename or Text List

@return: two files differents
'''
def compare_content(src_content, dst_content):
    changed_list = []
    
    if type(src_content) == types.StringType and type(dst_content) == types.StringType:
        if not os.path.isfile(src_content) or not os.path.isfile(dst_content):
            return []
        compare_list = diff_file(src_content, dst_content)
    elif type(src_content) == types.ListType and type(dst_content) == types.ListType:
        compare_list = diff_text(src_content, dst_content)
    
    if compare_list == None:
        compare_list = []
    
    for compare_item in compare_list:
        
        if compare_item.get('tag') == 'replace':
            src_item_list = compare_item.get('src_item')
            dst_item_list = compare_item.get('dst_item')
            if len(src_item_list) == len(dst_item_list):
                for i in range(len(src_item_list)):
                    changed_list.append({'src': src_item_list[i], 'dst': dst_item_list[i], 'action': 'changed'})
                    
        elif compare_item.get('tag') == 'delete':
            item_list = compare_item.get('src_item')
            for item in item_list:
                changed_list.append({'src': item, 'action': 'delete'})
                
        elif compare_item.get('tag') == 'insert':
            item_list = compare_item.get('dst_item')
            for item in item_list:
                changed_list.append({'dst': item, 'action': 'create'})
                    
    return changed_list

'''
group and statistics comapre result
'''
def get_compare_summary(compare_list):
    summary = {}
    
    for compare_item in compare_list:
        if compare_item.has_key('action'):
            action = compare_item.get('action')
            if action in ['create', 'delete', 'changed']:
                summary[action] = summary.get(action) + 1 if summary.has_key(action) else 1
    
    return summary

'''
compare differnet between two files

@param src_filename: Source Filename
@param dst_filename: Destination Filename  

@return: two files differents
'''
def diff_file(src_filename, dst_filename):
    
    if not os.path.isfile(src_filename) or not os.path.isfile(dst_filename):
        return None
    
    src_file = file(src_filename, 'r')
    dst_file = file(dst_filename, 'r')
    src_file_context = src_file.read()
    dst_file_context = dst_file.read()
    src_file_context = src_file_context.splitlines()
    dst_file_context = dst_file_context.splitlines()
    
    return diff_text(src_file_context, dst_file_context)

'''
compare differnet between two string

@param src_context: Source Text List
@param dst_context: Destination Text List  

@return: two string differents
'''  
def diff_text(src_content, dst_content):
    
    src_content = [src_text.strip() for src_text in src_content]
    dst_content = [dst_text.strip() for dst_text in dst_content]
    
    seq_matcher = difflib.SequenceMatcher(None, src_content, dst_content)
    diff_list = []
    for tag, src_start, src_end, dst_start, dst_end in seq_matcher.get_opcodes():
        diff_result = {}
        diff_result['tag'] = tag
        diff_result['src_start'] = src_start
        diff_result['src_end'] = src_end
        diff_result['src_item'] = src_content[src_start : src_end]
        diff_result['dst_start'] = dst_start
        diff_result['dst_end'] = dst_end
        diff_result['dst_item'] =  dst_content[dst_start : dst_end]
        
        diff_list.append(diff_result)
        
    return diff_list

