#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import glob
import fnmatch

from conf.config import conf

CURRENT_PATH = os.path.dirname( os.path.realpath(__file__) )
DATA_FILE = CURRENT_PATH + '/tmp/data.txt'

def findFile( dirname, filename ):
    ext = ".java"
    filename = filename if filename.endswith( ext ) else ( filename + ext )
    os.chdir( dirname )
    for root, dirnames, filenames in os.walk( dirname ):
        for codeFile in fnmatch.filter( filenames, '*' + ext ):
            path = os.path.join(root, codeFile )
            if codeFile == filename :
                return path
    return None


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


def save_file( filename, data ):
    if not os.path.exists( filename ):
        return False
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
        else:
            print "保存临时文件失败！"


if __name__ == "__main__":
    main(sys.argv)  
