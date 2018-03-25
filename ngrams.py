#!/usr/bin/env python3

import itertools
import re
import string

from collections import Counter, deque


def dialogs(lines):
    """
    Extract the dialogues from lines
    :param lines: Generator object containing lines of HTML page
    :return: Yield lines if they match dialog's regular expression.
    """
    r = re.compile(r'<A NAME=\d+\.\d+\.\d+>(.*)</A><br>')
    for line in lines:
        for match in r.finditer(line):
            yield match.groups(0)[0]


def nopunct(lines):
    """
    Remove punctuations from a set of lines
    :param lines: Lines with punctuations
    :return: Yield a line without punctuation
    """
    table = {ord(c): None for c in set(string.punctuation) - {"'"}}
    for line in lines:
        line = line.translate(table)
        if line:
            yield line


def words(lines):
    """
    Split the lines into words
    :param lines: Lines
    :return: Yield words after stripping punctuations
    """
    for line in nopunct(lines):
        for word in line.split():
            yield word.strip().lower()


def ngrams(lines, n):
    """
    Take the lines and yield n-grams from it
    :param lines: Lines
    :param n: Size of each n-gram
    :return: Yield each n-gram one after another
    """
    dq = deque(maxlen=n)
    w_gen = words(lines)
    # Add N - 1 elements to dq
    for _ in itertools.repeat(None, n - 1):
        dq.append(next(w_gen))
    for word in w_gen:
        dq.append(word)
        yield ' '.join(dq)


def parse_and_gen(file_name, ngram_count, item_count):
    """
    Helper function to read and find the most common words
    :param file_name: File name having novel
    :param ngram_count: N-gram size
    :param item_count: Number of most common items to return
    :return: Yield the counter's top N most common items
    """
    with open(file_name) as lines:
        counter = Counter(gram for gram in ngrams(dialogs(lines), ngram_count))
        for item in counter.most_common(item_count):
            yield item


if __name__ == '__main__':
    # all.html was taken from http://shakespeare.mit.edu/allswell/full.html
    for i, ng in enumerate(parse_and_gen('all.html', 4, 10)):
        print(i + 1, ng)
