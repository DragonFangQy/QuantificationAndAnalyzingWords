
import itertools
import os

from Levenshtein import distance, ratio

words_list = ["narrow", "narrowA", "sorrow", "borrow", "borrowA", "borrowB", "arrow", "row", "precision"]


class SimilarWord(object):
    def __init__(self, word, similar_list):
        self.word = word
        self.similar_list = similar_list

    def __str__(self):
        # ### aa
        # > bbb bbb bbb bbb bbb

        line_format = "> %s %s %s %s %s"

        dispose_size = 5
        quotient, remainder = len(self.similar_list) // dispose_size, len(self.similar_list) % dispose_size
        counter = quotient + 1 if remainder > 0 else quotient

        result_list = []

        result_list.append("### %s" % self.word)

        for loop in range(counter):
            result_list.append(line_format % self.similar_list[loop * dispose_size:(loop + 1) * dispose_size])

        return "\n".join(result_list)


def compute_similar_score(string1, string2, switch_value=3):
    """
    计算相似度

    通过 Levenshtein 的 distance 和 ratio

    :param string1:
    :param string2:
    :param switch_value: 临界值 , distance 的值大于临界值取 ratio 的结果 ,否则 相似度 为 1
    :return:[0,1]
    """
    score_distance = distance(string1, string2)

    if score_distance > switch_value:
        return ratio(string1, string2)

    return 1


def marge_word_file(marge_file_path):
    """
    合并单词文件并去重

    :return:
    """

    word_file_path_list = []
    word_list = []
    for root, dirs, files in os.walk("../word"):
        for file in files:
            word_file_path_list.append(root + "/" + file)

    for word_file_path in word_file_path_list:
        with open(word_file_path, "r") as rf:
            word_list.extend(rf.readlines())

    word_list.sort()
    with open(marge_file_path, "w") as wf:
        for word, grouper in itertools.groupby(word_list):
            if word == "\n":
                continue
            wf.write(word)


if __name__ == '__main__':
    # for item in words_list[:]:
    #     item_seq1 = item
    #     item_seq2 = words_list[:]
    #     item_seq2.remove(item)
    #
    #     for item_b in item_seq2:
    #         str1 = item_seq1
    #         str2 = item_b
    #
    #         print(str1, '\t', str2)
    #         print(compute_similar_score(str1, str2))
    #
    #         print()
    #
    #     print()
    #     print("--" * 20)
    #     print()
    marge_word_file("../word/002_marge_file.word")
