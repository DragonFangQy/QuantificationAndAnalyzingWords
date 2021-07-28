from io import StringIO

import re

import itertools
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


class PDFParse(object):

    def __init__(self, pdf_file_name, file_path, page_range: tuple = (20, 149)):
        """

        :param pdf_file_name:
        :param file_path:
        :param page_range:
        """

        self.pdf_file_name = pdf_file_name
        self.page_range = page_range
        self.file_path = file_path

    @staticmethod
    def get_cet_test_vocabulary(pdf_file_name, page_range: tuple):
        """
        通过考试大纲 pdf , 获取考试词汇

        :param pdf_file_name: 文件名
        :param page_range: 元组 , [起始页码,结束页码) , 从 0 开始计数
        :return:
        """

        output_string = StringIO()
        with open(pdf_file_name, 'rb') as in_file:
            parser = PDFParser(in_file)
            doc = PDFDocument(parser)

            rsrcmgr = PDFResourceManager()
            device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
            interpreter = PDFPageInterpreter(rsrcmgr, device)

            for (pageno, page) in enumerate(PDFPage.create_pages(doc)):

                if pageno in range(*page_range):
                    interpreter.process_page(page)

                if pageno >= page_range[1]:
                    break

        return output_string.getvalue()

    def write_file(self, file_path, content: list):
        """
        将解析的结果处理后 写入文件

        :return:
        """

        # afterward(s)   写两行  afterward\nafterwards
        # airplane/aeroplane 写两行  airplane\naeroplane
        # air-conditioning air-conditioner 写两行 air-conditioning\nair-conditioner
        # apologize/-ise apologetic 写三行     apologize\napologise\napologetic
        with open(file_path, "w", encoding="utf8") as wf:

            for line_ in content:
                line_ = self.special_handle(line_)

                if line_ is None:
                    continue

                wf.write(line_ + "\n")

    @staticmethod
    def special_handle(string):
        """
        对解析的PDF 内容进行特殊处理

        :param string:
        :return:
        """

        result_str = ""

        re_search = re.search("[A-Za-z]+", string)

        if re_search is None or re_search.group() == "":
            return None

        # 'bound１'
        string = re.sub("\d+", "", string)

        # apt．
        string = re.sub("．", "", string)

        # coup(d􀆳état)
        string = re.sub("\(d􀆳état\)", "", string)

        # air-conditioning air-conditioner 写两行 air-conditioning\nair-conditioner
        string = re.sub("\s+", "\n", string)

        # afterward(s)   写两行  afterward\nafterwards
        if "(" in string:
            print(string)
            re_match = re.match("(.*?)(\(.*?\))(.*)", string)
            result_str += re_match.group(1) + re_match.group(3) + "\n"
            result_str += string.replace("(", "").replace(")", "")
            return result_str

        if string.count("/") > 0 and string.count("/-") == 0:
            result_str = string.replace("/", "\n")
            return result_str

        # advisor/-er
        if string.count("/-") > 0:
            word_list = string.splitlines()

            for word in word_list[:]:
                if "/-" in word:
                    word1 = word.split("/-")[0]
                    word_endwith = word.split("/-")[1]
                    word2 = word1[:-len(word_endwith)] + word_endwith

                    word_list.remove(word)
                    word_list.append(word1)
                    word_list.append(word2)

            result_str = "\n".join(word_list)
            return result_str

        return string

    @staticmethod
    def remove_duplication_word(file_path):
        """
        对文件内容去重

        :param file_path:
        :return:
        """

        with open(file_path, "r") as rf:
            rf_list = rf.readlines()
            rf_list.sort()

            with open(file_path, "w") as wf:
                for word, grouper in itertools.groupby(rf_list):
                    if word == "\n":
                        continue
                    wf.write(word)

    def run(self):

        parse_result = self.get_cet_test_vocabulary(self.pdf_file_name, self.page_range)

        # 特殊处理: - 会被解析为 Ｇ
        parse_result = parse_result.replace("Ｇ", "-")
        parse_result_list = parse_result.splitlines()

        self.write_file(self.file_path, parse_result_list)

        self.remove_duplication_word(self.file_path)
        print(parse_result)


if __name__ == '__main__':
    pdf_parse = PDFParse("55b02330ac17274664f06d9d3db8249d.pdf", "../../word_file/pdf_parse.word")
    pdf_parse.run()
