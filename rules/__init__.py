#coding=utf-8

import iptable14 as rulesobj

def get_rules_info():
    return rulesobj.Rules().get_rules_info()

