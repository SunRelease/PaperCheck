# -*- coding: utf-8 -*-
# author :HXM

from sys import argv
import math, logging
import jieba
import jieba.analyse
from simhash import Simhash

# 输出日志设置
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [line:%(lineno)d] - %(levelname)s: %(message)s')


class SimHash(object):
    '''
    对文件进行执行分词,降维
    '''
    def get_source_string(self, source):
        '''
        获取原字符串
        :param source:
        :return:
        '''
        if source == "":
            return 0
        else:
            x = ord(source[0]) << 7
            m = 1000003
            mask = 2 ** 128 - 1
            for c in source:
                x = ((x * m) ^ ord(c)) & mask
            x ^= len(source)
            if x == -1:
                x = -2
            x = bin(x).replace('0b', '').zfill(64)[-64:]
            return str(x)






