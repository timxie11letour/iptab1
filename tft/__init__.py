#coding=utf-8

import tft_awk
import tft_grep
import tft_sed
import tft_diff
import txtfile
import key_map

def awk(regex, target, split, column):
    return tft_awk.awk(regex, target, split, column)
    
def grep(regex, target, model, number=False):
    return tft_grep.grep(regex, target, model, number)

def sed(regex, model, replace, target, operate, output):
    return tft_sed.sed(regex, model, replace, target, operate, output)

def compare_file_list(src_file_list, dst_file_list, compare_fun):
    return tft_diff.compare_file_list(src_file_list, dst_file_list, compare_fun)

def compare_content(src_content, dst_content):
    return tft_diff.compare_content(src_content, dst_content)

def get_compare_summary(compare_list):
    return tft_diff.get_compare_summary(compare_list)

def diff_file(src_filename, dst_filename):
    return tft_diff.diff_file(src_filename, dst_filename)

def diff_text(src_text, dst_text):
    return tft_diff.diff_text(src_text, dst_text)

def map_str(string, split, keys):
    return key_map.map_str(string, split, keys)

def load_file_as_list(filename):
    return txtfile.load_file_as_list(filename)

def load_file(filename):
    return txtfile.load_file(filename)

def save_file(filename, file_content_list):
    txtfile.save_file(filename, file_content_list)

def load_property(filename):
    return txtfile.load_property(filename)

def save_property(filename, config):
    txtfile.save_property(filename, config)