import itertools
import os

from Levenshtein import distance, ratio

from words.word import Word


class SimilarWord(object):
    def __init__(self, check_similar_path, word=None, distance_switch_value=2,
                 similar_switch_value=0.9
                 , similar_result_file_path=None
                 ):
        """
        :param word: 主词 , 判定主词 和 副词文件内的单词  是否相似
                    , 如果不指定主词
                    , 则通过 check_similar_file_name 获取主词
                    , 即 check_similar_file_name 文件内的每一个次都作为主词
                    , 和其它单词进行比较


        :param check_similar_path: 副词文件路径 , 副词相对主词而言

        :param distance_switch_value: 编辑临界值
                                    , distance 小于等于 distance_switch_value 相似度 为 1
                                    , 否则 取 ratio 的结果 ,

                                    例:
                                    narrow	borrow   distance_switch_value=3
                                    distance:2	ratio:0.6666666666666666

                                    ratio 仅为 0.67
                                    如果以0.9 为界限, narrow 与 borrow 必然不满足相似
                                    ,所以加入 distance & switch_value
                                    ,通过 distance=2 <= distance_switch_value=3 相似度为 1
                                    ,1 > similar_switch_value=0.9
                                    ,判定相似


        :param similar_switch_value: 相似临界值
                                    , >=similar_switch_value 判定相似


        :param similar_result_file_path: 相似结果保存的文件路径
                                    , None 不保存



        """

        self.word = word

        # 副词文件路径
        self.check_similar_path = check_similar_path

        # 存放 check_similar_file_name 内的单词
        self.check_similar_list = []

        # 存放相似单词
        self.similar_list = []

        # 存放 similar_list 的文件
        self.similar_result_file_path = similar_result_file_path

        # 编辑临界值
        self.distance_switch_value = distance_switch_value

        # 相似临界值
        self.similar_switch_value = similar_switch_value

    def marge_word_file(self, check_similar_file_name_path):
        """
        合并单词文件并去重

        :param check_similar_file_name_path: 副词文件路径  , 副词相对主词而言
                                    , 将 check_similar_path 下的所有副词文件合并
                                    , 得到所有待检单词
                                    , 将这些单词写入 check_similar_file_name.word 文件内
                                    , 如果 check_similar_file_name=None
                                    , 则不写入文件

        :return:
        """

        # check_similar_file_name_path != None and check_similar_file_name_path!=''
        if check_similar_file_name_path is None or len(check_similar_file_name_path.strip()) == 0:
            return

            # 删除历史文件
        if os.path.isfile(check_similar_file_name_path):
            os.remove(check_similar_file_name_path)

        word_file_path_list = []
        word_list = []
        strip_str = "\n"

        # 获取副词目录下 word 文件
        for root, dirs, files in os.walk(self.check_similar_path):  # "../word"):
            for file in files:
                if file.endswith("word"):
                    word_file_path_list.append(root + file)

        # 获取文件内容
        for word_file_path in word_file_path_list:
            with open(word_file_path, "r") as rf:
                word_list.extend(rf.readlines())

        # 内容去重并写入文件
        word_list = sorted(list(set(word_list)))

        for word in word_list:
            word = word.strip(strip_str)

            # of an CD 等单词直接去除
            if len(word) < self.distance_switch_value:
                continue

            # 将去重后的内容村存入 check_similar_list
            self.check_similar_list.append(word)

        # 写入文件
        with open(check_similar_file_name_path, "a+") as wf:
            wf.write("\n".join(self.check_similar_list))
            wf.write("\n")

    def word_no_exists(self):
        """
        主词不存在

        :return:
        """

        # 通过 file_path 控制写入文件
        # 如果 file_path == "__similar_result_file_path__"
        #       则 删除__similar_result_file_path__ , 即不写入文件

        # 首先给予一个文件名
        file_path = "__similar_result_file_path__"

        # 如果 similar_result_file_path 存在则 file_path = similar_result_file_path
        if self.similar_result_file_path is not None:
            file_path = self.similar_result_file_path

        similar_word_list = []

        with open(file_path, "w") as wf:
            for w1_index in range(len(self.check_similar_list) - 1):

                # 获取单词 , 构造主词
                w1 = self.check_similar_list[w1_index]
                w1_sw = SimilarWord(self.check_similar_path, word=w1)

                for w2_index in range(w1_index + 1, len(self.check_similar_list)):

                    # 获取副词
                    word_2 = self.check_similar_list[w2_index]

                    # 判断和主词是否相似
                    if self.is_similar(w1_sw.word, word_2):
                        w1_sw.similar_list.append(word_2)

                wf.write(w1_sw.get_str())
                wf.write("\n\n")
                similar_word_list.append(w1_sw)

        # 不写文件 ,返回数组
        if file_path == "__similar_result_file_path__":
            os.remove(file_path)
            return similar_word_list

        # 写文件,返回空数组
        return []

    def word_exists(self):
        """
        主词存在

        :return:
        """

        # 通过 file_path 控制写入文件
        # 如果 file_path == "__similar_result_file_path__"
        #       则 删除__similar_result_file_path__ , 即不写入文件

        file_path = "__similar_result_file_path__"

        if self.similar_result_file_path is not None:
            file_path = self.similar_result_file_path

        with open(self.similar_result_file_path, "w") as wf:
            for check_word in self.check_similar_list:
                if self.is_similar(self.word, check_word):
                    self.similar_list.append(check_word)

            wf.write(self.write_file())
            wf.write("\n")

        # 不写文件 ,返回数组
        if file_path == "__similar_result_file_path__":
            os.remove(file_path)
            return [self]

        # 写文件,返回空数组
        return []

    def is_similar(self, string1, string2):
        """
        判定是否相似

        通过 Levenshtein 的 distance 和 ratio

        如果 len(string1) + len(string2) 小于等于 distance_switch_value * 2
        , 暂定 直接走 ratio
        , 即 len(string1) + len(string2)> distance_switch_value * 2
        , 走 distance

        :param string1:
        :param string2:
        :return:[0,1]
        """

        score_distance = distance(string1, string2)

        # 编辑距离小于 等于临界值 , 相似度为 1
        # 即两词相似
        if score_distance <= self.distance_switch_value:
            return True

        score_ratio = ratio(string1, string2)
        # score_ratio >= similar_switch_value , 判定相似
        # 即两词相似
        if score_ratio >= self.similar_switch_value:
            return True

        # 不满足以上条件
        # 即两词不相似
        return False

    def write_file(self):
        """


        :return:
        """

        # aa
        # > bbb bbb bbb bbb bbb

        line_format = "\t "

        dispose_size = 5
        quotient, remainder = len(self.similar_list) // dispose_size, len(self.similar_list) % dispose_size
        counter = quotient + 1 if remainder > 0 else quotient

        Word(self.word)
        result_list = ["%s\n" % self.word]



        for loop in range(counter):
            format_list = self.similar_list[loop * dispose_size:(loop + 1) * dispose_size]
            format_list_len = len(format_list)
            line_format_str = line_format + "%s\t" * format_list_len
            result_list.append(line_format_str % tuple(format_list))

        return "\n".join(result_list)

    def run(self, check_similar_file_name):
        # 合并单词并去重
        self.marge_word_file(check_similar_file_name)

        # 读取 check_similar_list
        # word 判断主词
        # 主词存在
        #       则通过 主词 check_similar_list 判断相似
        # 否则 check_similar_list[i....n-1] 和 check_similar_list[i+1...n] 进行相似判断

        # 主词存在
        if self.word is not None:
            return self.word_exists()

        # 主词不存在
        return self.word_no_exists()


if __name__ == '__main__':
    word_files_path = "../word_file/"
    sw = SimilarWord(word_files_path,
                     similar_result_file_path=word_files_path + "001_similar_word.txt")
    sw.run(check_similar_file_name=word_files_path + "002_marge_file.txt")
