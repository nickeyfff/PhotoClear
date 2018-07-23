# -*- coding: utf-8 -*-  

""" 
查找_1024.jpg 结尾的文件. 移到另外一个地方. 或者删掉
"""  

import shutil  
import os  
import time  
import exifread  
import re
from datetime import datetime

class ReadFailException(Exception):  
    pass  


allNumber=0
def find1024(path):  
    # print "path:"+path
    for root,dirs,files in os.walk(path,True):  

        for name in dirs:
            # print "pricess dir:"+os.path.join(root, name)
            find1024(os.path.join(root, name))
        dirs[:] = []  
        for filename in files:
            originalFilename=filename
            filename = os.path.join(root, filename)  
            pathAndFilename,fileExt = os.path.splitext(filename)
            # print "1:"+pathAndFilename
            if filename.find("_1024.jpg") >0:
                # if(os.path.exists(filename)):
                    print "2:%s %d" % (filename,os.path.getsize(filename))
                    dst="../backup"+os.sep+originalFilename
                    print dst
                    # shutil.move( filename, dst)
            
        
if __name__ == "__main__":  
    path = "."  
    find1024(path)  
    
