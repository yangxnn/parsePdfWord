# coding:utf-8
import operator
import sys
import os
from functools import reduce

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox

INVALID_CHAR = ['(', ')', '+', '=', '*', '-', '@', '%', '^', '[', ']', '{', '}', '/', ',', '.', ';', ':', '<', '>', '?',
                '!']


def filter1(word):
    if len(word) < 3:
        return False
    for c in INVALID_CHAR:
        if c in word:
            return False
    return True


def reduceWord(word2count, word):
    if word not in word2count:
        word2count[word] = 0
    word2count[word] += 1
    return word2count


def parsePaper(path, percentile=100):
    doc = PDFDocument()
    resWords = []
    with open(path, 'rb') as parse:
        parser = PDFParser(parse)
        parser.set_document(doc)
        doc.set_parser(parser)
        device = PDFPageAggregator(PDFResourceManager(), laparams=LAParams())
        interpreter = PDFPageInterpreter(PDFResourceManager(), device)
        for page in doc.get_pages():
            interpreter.process_page(page)
            layout = device.get_result()
            for x in layout:
                if isinstance(x, LTTextBox):
                    resWords += x.get_text().split(' ')
    resWords = map(lambda x: x.lower(), resWords)
    resWords = map(lambda x: x.strip(), resWords)
    resWords = filter(lambda x: filter1(x), resWords)
    word2count = reduce(lambda x, y: reduceWord(x, y), resWords, {})
    sortedWordCount = sorted(word2count.items(), key=operator.itemgetter(1), reverse=True)
    print(sortedWordCount[:20])

    outfile = path.split('/')[-1].split('.')[0]
    with open('%s.txt' % outfile, 'w') as fo:
        for words in sortedWordCount:
            try:
                fo.write('%s\n' % words[0])
            except Exception:
                print('exception word:%s' % words[0])


if __name__ == '__main__':
    filePath = sys.argv[1]
    percentile = sys.argv[2]
    parsePaper(filePath, percentile)
