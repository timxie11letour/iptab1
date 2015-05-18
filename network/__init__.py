#coding=utf-8

import policy

def analyse_policy_compare(src_policy_group, dst_policy_group = None, deny_ignore = True):
    return policy.analyse_policy_compare(src_policy_group, dst_policy_group, deny_ignore)

def analyse_policy_scope(policy_group, deny_ignore=True):
    return policy.analyse_policy_scope(policy_group, deny_ignore)

def anaylse_policy_outdate(policy_group):
    return policy.anaylse_policy_outdate(policy_group)

def anaylse_unused_object(used_object_list, object_group):
    return policy.anaylse_unused_object(used_object_list, object_group)