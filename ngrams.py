#!/usr/bin/env python3
"""
Module that can generate N-Grams from a Shakespear's play
"""
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
    regex = re.compile(r'<A NAME=\d+\.\d+\.\d+>(.*)</A><br>')
    for line in lines:
        for match in regex.finditer(line):
            yield match.groups(0)[0]

PUNCTUATION_TABLE = {ord(c): None for c in set(string.punctuation) - {"'"}}

def clean(word):
    """
    Remove punctuations and whitespaces from a word, finally lowercase
    the word and yield it.

    :param word: Word with punctuations
    :return: Yield a word without punctuation
    """
    return word.translate(PUNCTUATION_TABLE).strip().lower()


def words(line):
    """
    Split the line into words, remove punctuations and whitespaces
    and finally lowercase the word and yield it
    :param lines: Line of text
    :return: Yield words
    """
    regex = re.compile(r'(\w+)')
    for match in regex.finditer(line):
        yield match.group(0)


def ngrams(iwords, num):
    """
    Take the lines and yield n-grams from it
    :param iwords: Words iterator
    :param n: Size of each n-gram
    :return: Yield each n-gram one after another
    """
    dq_words, iwords = itertools.tee(iwords)
    # Add N - 1 elements to deque, deque has max len of N in n-grams
    d_q = deque(itertools.islice(dq_words, num - 1), maxlen=num)
    for word in itertools.islice(iwords, num - 1, None):
        d_q.append(word)
        yield ' '.join(d_q)


def parse_and_gen(file_name, ngram_count, item_count):
    """
    Helper function to read the play, extract dialogs, then
    remove punctuations and finally split lines into words and
    geneate n-grams
    :param file_name: File name having Shakespear's plays in a certain format
    :param ngram_count: N-gram count for N
    :param item_count: Number of most common items to return
    :return: Yield the counter's top N most common items
    """
    with open(file_name) as lines:
        word_gen = (word for line in dialogs(lines) for word in words(line))
        counter = Counter(gram for gram in ngrams(word_gen, ngram_count))
        for item in counter.most_common(item_count):
            yield item


if __name__ == '__main__':
    # The file "all.html" was taken from
    # http://shakespeare.mit.edu/allswell/full.html
    for i, ng in enumerate(parse_and_gen('all.html', 4, 10)):
        print(i + 1, ng)
