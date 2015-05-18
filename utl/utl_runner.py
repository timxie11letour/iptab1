#coding=utf-8

'''
Created on 2013-1-25

@author: Huiyugeng
'''

import ndb
import regex

import imp
import types
import sys

'''
execute test script
'''
def run(filename):
    result = []
    
    test_suite = ndb.load(filename)
    test_suite = test_suite if type(test_suite) == types.ListType else [test_suite]
    
    for test in test_suite:
        module_list = ndb.query('test->module', test, True)
        
        result.extend(get_module(module_list))
    
    return result

'''
get module info from script
'''
def get_module(module_list):
    result = []
    
    module_list = module_list if type(module_list) == types.ListType else [module_list]
    
    for module in module_list:
        module_name = module.get('name')
        if module_name == None:
            return
        
        module_path = module.get('path') if module.has_key('path') else ''
        
        class_list = module.get('class') if module.has_key('class') else []
        result.extend(get_class(module_path, module_name, class_list))
    
        function_list = module.get('function') if module.has_key('function') else []
        result.extend(get_function(module_path, module_name, None, function_list))
    
    return result

'''
get class info from moule description
'''
def get_class(module_path, module_name, class_list):
    result = []
    
    class_list = class_list if type(class_list) == types.ListType else [class_list]
    
    for class_item in class_list:
        class_name = class_item.get('name')
        function_list = class_item.get('function') if class_item.has_key('function') else []
        result.extend(get_function(module_path, module_name, class_name, function_list))
    
    return result

'''
get class info from class or module description
'''
def get_function(module_path, module_name, class_name, function_list):
    
    result = []
    
    function_list = function_list if type(function_list) == types.ListType else [function_list]
    for function_item in function_list:
        function_name = function_item.get('name')
        param_list = get_param(function_item)
        result_value = invoke_function(module_path, module_name, class_name, function_name, param_list)
        
        result.append(check_result(function_item, result_value))
        
    return result

'''
build function parameters
'''       
def get_param(function):
    params = []
    
    param_list = function.get('param') if function.has_key('param') else []
    param_list = param_list if type(param_list) == types.ListType else [param_list]
    
    for param in param_list:
        param_type = param.get('type') if param.has_key('type') else 'str'
        param_value = param.get('value')
        if param_value != None:
            param_value = convert_value(param_type, param_value)
            params.append(param_value)
        else:
            params.append(None)
    
    return params

'''
check function execute result
'''
def check_result(function, result_value):
    result = []
    
    check_list = function.get('result') if function.has_key('result') else []
    check_list = check_list if type(check_list) == types.ListType else [check_list]
    
    for check_item in check_list:
        if 'name' in check_item and 'operate' in check_item:
            check_name = check_item.get('name')
            check_value = convert_value(check_item.get('type'), check_item.get('value'))
            operate = check_item.get('operate')
            
            _result = False
            if operate == 'len': #check result length
                _result = (check_value == len(result_value))
            elif operate == 'in': #check expect value in result 
                _result = (check_value in result_value)
            elif operate == 'query': #query result
                query_exp = check_item.get('query')
                result_value = ndb.query(query_exp, result_value, True)
                _result = (check_value == result_value)
            elif operate == 'regex_check': #use regex check result
                regex_exp = check_item.get('regex')
                _result = regex.check_line(regex_exp, result_value)
            elif operate == 'regex_equal': #use regex equal result
                regex_exp = check_item.get('regex')
                result_value = regex.get_line(regex_exp, result_value)
                _result = (check_value == result_value)
            else: #equal value
                operate = 'equal'
                _result = (check_value == result_value)
            
            if _result:
                result.append({'name':check_name, 'result':_result})
            else:
                result.append({'name':check_name, 'result':_result, 'operate': operate , 'expect_value': check_value, 'result_value': result_value})
    
    return result
        
'''
convert value to another type value
'''
def convert_value(value_type, value):
    result = None
    
    if value_type == 'int':
        result = int(value)
    elif value_type == 'float':
        result = float(value)
    elif value_type == 'long':
        result = long(value)
    elif value_type == 'bool':
        result = bool(value)
    elif value_type in ['dict' ,'list' ,'tuple', 'object']:
        result = eval(value)
    else:
        result = value
    
    return result

'''
invoke function in class or module
'''
def invoke_function(module_path, module_name, class_name, function_name, arg):
    try:
        if module_path != None and module_path != '':
            module_path_list = module_path.split(';')
            sys.path.extend(module_path_list)
        
        file, path, desc = imp.find_module(module_name)
        module = imp.load_module(module_name, file, path, desc)
        
        if class_name!=None:
            clazz = module.__dict__.get(class_name)
            function = clazz.__dict__.get(function_name)
            result = function(clazz, *arg)
        else:
            function = module.__dict__.get(function_name)
            result = function(*arg)
    except:
        pass
    
    return result
    
    
        