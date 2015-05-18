#coding=utf-8

import regex

def get_line(regex_str , line):
    return regex.get_line(regex_str, line)

def check_line(regex_str, line):
    return regex.check_line(regex_str, line)

def sub(regex_str, repl_str, line, count=0):
    return regex.sub(regex_str, repl_str, line, count)

def split(regex_str, line):
    return regex.split(regex_str, line)