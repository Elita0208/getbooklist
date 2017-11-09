# -*- coding: utf-8 -*-
import os
import sys
from datetime import date
from scrapy import cmdline
from optparse import OptionParser

if __name__ == '__main__':
    baseDir = os.path.split(os.path.realpath(__file__))[0]
    logdir = os.path.join(baseDir, 'log', date.today().strftime('%Y-%m-%d'))

    #usage: python main.py -s Douban
    usage = "usage: %prog [options] arg1 arg2"   #%prog optparse 会以当前程序名的字符串来替代
    version = "%prog 1.0"
    #创建一个 OptionParser 对象
    parser = OptionParser(usage=usage, version=version)

    #使用 add_option 来定义命令行参数
    parser.add_option("-s", "--spider", action="store", dest="spider", default='all',
                      help="Douban|Zhihu")
    parser.add_option("-l", "--logdir", action="store", dest="logdir", default=logdir)

    #定义好了所有的命令行参数，调用 parse_args() 来解析程序的命令行
    (options, args) = parser.parse_args()
    spider = options.spider
    logdir = options.logdir

    if not os.path.isdir(logdir):
        os.makedirs(logdir)

    if spider == 'all':
        for spider in ['Douban','Zhihu']:
            logpath = os.path.join(logdir, spider+'.log')  #日志路径
            cmdstr = "scrapy crawl "+spider +' --logfile='+logpath  #scrapy crawl -h查看帮助
            print(cmdstr)
            cmdline.execute(cmdstr.split())
    else:
        logpath = os.path.join(logdir, spider+'.log')
        cmdstr = "scrapy crawl "+spider +' --logfile='+logpath
        print(cmdstr)
        cmdline.execute(cmdstr.split())
