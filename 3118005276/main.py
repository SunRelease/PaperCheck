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


class PaperCheck():
    '''
    论文查重类
    '''

    def get_simlar_text(self, text1, text2):
        '''
        1.文本相似度比较算法
        2.使用simhash分析
        :param text1:
        :param text2:
        :return:
        '''
        new_simhash = SimHash()

        hash_first = new_simhash.getHash(text1)  # 计算hash值
        hash_second = new_simhash.getHash(text2)

        text_first_hash = Simhash(hash_first)
        text_second_hash = Simhash(hash_second)

        distince = text_first_hash.distance(text_second_hash)

        max_hashbit = max(len(bin(text_first_hash.value)), (len(bin(text_second_hash.value))))

        if max_hashbit == 0:
            return 0
        else:
            similar = 1 - distince / max_hashbit
            return (similar)

    def check_similar(self, argv):
        '''
        1.比较相似度
        :param argv:
        :return:
        '''
        try:

            origin_article = open(argv[1], 'rt', encoding='utf-8')  # 源文件

            copies_article = open(argv[2], 'rt', encoding='utf-8')  # 抄袭文件

            answer = open(argv[3], 'a+', encoding='utf-8')  # 结果保存

            origin_article_source = origin_article.read()

            copies_article_source = copies_article.read()

            similar = self.get_simlar_text(origin_article_source, copies_article_source)  # 对比相似度

            similar = round(similar, 2)  # 精确到两位小数点

            strs = "两篇文章(" + argv[1] + " & " + argv[2] + ")\n相似率为："

            answer.write(strs + str(similar) + "\n")

            logging.info("两篇文章相似率为：%.2f\n结果已经存入指定文档" % similar)
            '''
            关闭文件,释放资源
            '''
            origin_article.close()
            copies_article.close()
            answer.close()
        except IndexError:
            logging.error("参数输入错误,请重新输入！")
        except FileNotFoundError:
            logging.error("没找到文件,输入错误,请重新输入！")
        except Exception as e:
            logging.error(f"未知错误：{e}")
        return 0


if __name__ == '__main__':

    # 命令行用法：
    # python .\main.py .\test\test\orig.txt .\test\test\orig_0.8_dis_15.txt .\test\test\check.txt
    papercheck = PaperCheck()
    # argv=['.\\main.py','.\\test\\orig.txt','.\\test\\orig_0.8_add.txt','.\\test\\check.txt']
    papercheck.check_similar(argv)
