#coding=utf-8

'''
Created on 2014-10-11

@author: Liangkangzhu
'''

from optparse import OptionParser

def get_option_parser():
    parser = OptionParser()  
    parser.add_option('-A', action='store', dest='addgroup')
    parser.add_option('-s', action='store', dest='srcaddress')
    parser.add_option('-d', action='store', dest='dstaddress')
    parser.add_option('-p', action='store', dest='protocol')
    parser.add_option('-m', action='store', dest='protocolm')
    parser.add_option('--sport', action='store', dest='sport')
    parser.add_option('--dport', action='store', dest='dport')
    parser.add_option('-j', action='store', dest='action')
    return parser

if __name__ == "__main__":
    arg_cmd = '-I INPUT 2 -s 192.168.2.5/32 -d 192.168.2.6/32 -p tcp -m tcp --sport 80 --dport 80:90 -j DROP'
    arg_cmd2 = '-A INPUT -s 192.168.2.5/32 -d 192.168.2.6/32 -j DROP'
    arg_cmd3 = '-A OUTPUT -s 192.168.2.5/32 -d 192.168.2.6/32 -p icmp -j DROP'
    
    opt, args =get_option_parser().parse_args(arg_cmd2.split(' '))
    
    print opt
    print args
    
    
