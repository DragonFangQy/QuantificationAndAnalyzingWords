from io import StringIO

from Levenshtein import distance, ratio
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

words_list = ["narrow", "narrowA", "sorrow", "borrow", "borrowA", "borrowB", "arrow", "row", "precision"]


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


def get_cet_test_vocabulary(pdf_file_name, page_no: tuple = (20, 149)):
    """
    通过考试大纲 pdf , 获取考试词汇

    :param pdf_file_name: 文件名
    :param page_no: 元组 , [起始页码,结束页码) , 从 0 开始计数
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

            if pageno in range(*page_no):
                interpreter.process_page(page)

            if pageno >= page_no[1]:
                break

    return output_string.getvalue()


if __name__ == '__main__':

    for item in words_list[:]:
        item_seq1 = item
        item_seq2 = words_list[:]
        item_seq2.remove(item)

        for item_b in item_seq2:
            str1 = item_seq1
            str2 = item_b

            print(str1, '\t', str2)
            print(compute_similar_score(str1, str2))

            print()

        print()
        print("--" * 20)
        print()
