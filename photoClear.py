# -*- coding: utf-8 -*-  

""" 
功能：对照片按照拍摄时间进行归类 
使用方法：将脚本和照片放于同一目录，双击运行脚本即可 
原作者：冰蓝
主要后续想处理osx中iphoto中的照片.
"""

import shutil
import os
import time
import exifread
import re
from datetime import datetime


class ReadFailException(Exception):
    pass


def getOriginalDate(filename):
    try:
        fd = open(filename, 'rb')
    except:
        raise ReadFailException, "unopen file[%s]\n" % filename
    data = exifread.process_file(fd)
    if data:
        try:
            t = data['EXIF DateTimeOriginal']
            return str(t).replace(":", "-")[:10]
        except:
            pass
    state = os.stat(filename)
    return time.strftime("%Y-%m-%d", time.localtime(state[-2]))


allNumber = 0
masterPattern = re.compile(ur'.+/Masters/.*')


def classifyPictures(path, destDir):
    global masterPattern;
    # print "path:"+path
    for root, dirs, files in os.walk(path, True):
        batchNumber = 0;
        for name in dirs:
            # print "pricess dir:"+os.path.join(root, name)
            # print name;
            classifyPictures(os.path.join(root, name), destDir)
        dirs[:] = []

        for filename in files:
            originalFilename = filename;
            filename = os.path.join(root, filename)
            # masterSearchObj=masterPattern.search(filename)
            # if( not masterSearchObj):
            #     continue

            pathAndFilename, fileExt = os.path.splitext(filename)
            if fileExt.lower() not in ('.jpg', '.png', '.mp4', '.bmp', ".cr2", ".avi", ".mov", ".mpg"):
                continue
            info = "文件名: " + filename + " "
            originalDateString = ""
            try:
                originalDateString = getOriginalDate(filename)
            except Exception, fileExt:
                print fileExt
                continue
            info = info + "拍摄时间：" + originalDateString + " "
            destDirectoryName = ""  # 定义输出的目录名称
            if '0000-00-00' == originalDateString:
                # 因为没有取到时间。 所以需要判断当前的目录是否已经安排了时间。
                pattern = re.compile(ur'(\d{4})-(\d{1,2})-(\d{1,2})$')
                searchObj = pattern.search(root)
                if searchObj:
                    # 目录里有日期。 取目录日期
                    dt = datetime(int(searchObj.group(1)), int(searchObj.group(2)), int(searchObj.group(3)))
                    # dirName=searchObj.group(1)+"-"+searchObj.group(2)+"-"+searchObj.group(3);
                    destDirectoryName = "%s-%s-%s" % (dt.strftime('%Y'), dt.strftime('%m'), dt.strftime('%d'))
                else:
                    destDirectoryName = 'other' + os.sep + os.path.basename(os.path.dirname(filename))
                    # 如果是放到other里, 需要把原来的目录名带上
            else:
                destDirectoryName = originalDateString

            pwd = destDir + os.sep + destDirectoryName

            dst = pwd + os.sep + originalFilename
            # print pwd
            if not os.path.exists(pwd):
                os.makedirs(pwd)
            if os.path.exists(dst):
                # 文件已经存在， 判断这个文件的大小. 如果比当前文件小,考虑覆盖过去
                dstFileSize = os.path.getsize(dst)
                originFileSize = os.path.getsize(filename)
                if (dstFileSize == originFileSize):
                    # print "file exist, pass"
                    os.remove(filename)
                    print "file exist! remove origin file:%s" % filename
                    continue
                elif originFileSize < dstFileSize:
                    print "file size less than dstFile, check:%s,%s" % (filename, dst)
                    continue
                else:
                    pass

            print info, dst

            # 如果是cr2结尾的文件,生成jpg到dst
            if fileExt.lower() == ".cr2":
                # print os.path.abspath(filename);   
                ff, ee = os.path.splitext(dst)
                # print ff;
                if (not os.path.exists(ff + ".JPG")):
                    command = "sips -s format jpeg \"%s\" --out \"%s\"" % (
                    os.path.abspath(filename), os.path.abspath(ff + ".JPG"))
                    print command
                    os.system(command)
                    # 检查目标文件是否存在, 如果存在,就代码cr2文件可以删除了.
                    # if os.path.exists(ff+".JPG"):
                    #     os.remove(ff+".JPG")
                    #     print "delete file:%s" % filename
                    #     pass
                    continue

            shutil.move(filename, dst)
            global allNumber
            allNumber += 1
            batchNumber += 1
            # os.remove( filename )  
        if batchNumber > 0:
            print "当前目录处理:%d" % batchNumber


if __name__ == "__main__":
    path = "."
    dstPath = ".." + os.sep + "dd"
    classifyPictures(path, dstPath)
    print "所有拷贝图片:%d" % allNumber
