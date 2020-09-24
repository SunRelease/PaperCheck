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

    def getHash(self, rawstr):
        '''
        对文章进行分词，降维
        :param rawstr:
        :return:
        '''
        seg = jieba.cut(rawstr)
        keywords = jieba.analyse.extract_tags("|".join(seg), topK=100, withWeight=True)
        ret = []
        for keyword, weight in keywords:
            '''
            获取关键字和权重
            '''
            source_str = self.get_source_string(keyword)
            keylists = []

            for c in source_str:
                weight = math.ceil(weight)
                if c == "1":
                    keylists.append(int(weight))
                else:
                    keylists.append(-int(weight))
            ret.append(keylists)
        rows = len(ret)
        # 对列表进行"降维"
        cols = len(ret[0])
        result = []
        for i in range(cols):
            tmp = 0
            for j in range(rows):
                tmp += int(ret[j][i])
            if tmp > 0:
                tmp = "1"
            elif tmp <= 0:
                tmp = "0"
            result.append(tmp)
        return "".join(result)





