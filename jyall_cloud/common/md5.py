#coding=utf-8
'''
Created on Mar 22, 2016

@author: root
'''
import hashlib

def getmd5(str):
    m1 = hashlib.md5()
    m1.update(str)
    return m1.hexdigest()