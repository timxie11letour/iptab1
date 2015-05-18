#coding=utf-8

'''
Created on 2012-10-30

@author: huiyugeng
'''
import os.path
import zipfile

'''
生成压缩文件
@param dirname: 需要压缩的目录
@param zipfilename: 压缩文件名称  
'''
def zip_dir(dirname, zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else :
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))
         
    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        #print arcname
        zf.write(tar, arcname)
    zf.close()

'''
解压文件
@param zipfilename: 压缩文件名
@param unziptodir: 解压目录 
''' 
def unzip_file(zipfilename, unziptodir):
    if not os.path.exists(unziptodir): os.mkdir(unziptodir, 0777)
    zfobj = zipfile.ZipFile(zipfilename)
    for name in zfobj.namelist():
        name = name.replace('\\', '/')
        if name.endswith('/'):
            os.mkdir(os.path.join(unziptodir, name))
        else:           
            ext_filename = os.path.join(unziptodir, name)
            ext_dir = os.path.dirname(ext_filename)
            if not os.path.exists(ext_dir) : os.mkdir(ext_dir, 0777)
            outfile = open(ext_filename, 'wb')
            outfile.write(zfobj.read(name))
            outfile.close()

'''
使用UNZIP命令解压文件
'''
def unzip_file_by_os(zipfilename, unziptodir):
    execute = os.popen('unzip {0} -d {1}'.format(zipfilename, unziptodir))
    result = execute.readlines()
    return result