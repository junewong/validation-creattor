#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------------
# 
# 用于根据Java的类代码，生成针对它的校验类
# e.g.
#   # 在配置的目录中查找类名对应的类：
#   python creator.py CommonDDL.java
#   # 明确指定路径来读取对应的类：
#   python creator.py ../ddl/CommonDDL.java
#
# @author junewong<wangzhu@ucweb.com>
# @date 2016-06-22
# --------------------------------------------------------------------------------

import os
import sys
import glob
import fnmatch

from conf.config import conf
from server.server import Server

CURRENT_PATH = os.path.dirname( os.path.realpath(__file__) )
DATA_FILE = CURRENT_PATH + '/tmp/data.txt'

# 查找文件
def findFile( dirname, filename ):
    if '/' in filename:
        if not os.path.exists( filename ):
            return None
        return filename

    ext = ".java"
    filename = filename if filename.endswith( ext ) else ( filename + ext )
    os.chdir( dirname )
    for root, dirnames, filenames in os.walk( dirname ):
        for codeFile in fnmatch.filter( filenames, '*' + ext ):
            path = os.path.join(root, codeFile )
            if codeFile == filename :
                return path
    return None


# 读取文件内容
def read_file( filename ):
    content = ''
    if not os.path.exists( filename ):
        return content
    f = None
    try:
        f = open( filename, 'r' )
        content = f.read()
    except Exception as e:
        raise e
    finally:
        if f is not None:
            f.close()
    return content


# 保存文件内容
def save_file( filename, data ):
    f = None
    try:
        f = open( filename, 'w' )
        f.write( data )
    except Exception as e:
        raise e
    finally:
        if f is not None:
            f.close()
    return True

def main(argv):
    if len(argv) > 1:
        className = argv[1]
        dirname = CURRENT_PATH + '/' + conf['root'] + conf['app']
        codeFile = findFile( dirname, className ) if len( argv ) <= 2 else argv[2]

        if not codeFile:
            print "找不到对应的类路径：" + className
            return
        print '找到目标类：'  + codeFile
        data = read_file( codeFile )
        if save_file( DATA_FILE, data ):
            print "保存临时文件成功"
            Server.run()
        else:
            print "保存临时文件失败！"
    else:
        print "没有指定目标类，根据之前的记录启动服务器……"
        Server.run()


if __name__ == "__main__":
    main(sys.argv)  
