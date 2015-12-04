# coding=utf-8
import re
import random
from os import listdir


def read_data_and_count_first_words_in_sentence():
    count_dots = 0
    flag = 0
    first_words_counter = {}
    re_not_letters = re.compile(r'[^a-zA-Z!\.,\?\']+')
    words = []
    files = listdir("./asimov")
    mytxt = filter(lambda x: x.endswith('.txt'), files)
    for corpus in mytxt:
        data = open("./asimov/" + corpus)
        for line in data:
            line = line.replace('\n', '')
            if len(line) > 0:
                for symbol in ["!", ".", "?", ","]:
                    line = line.replace(symbol, ' ' + symbol + ' ')
                line = re_not_letters.split(line)
                for word in line:
                    if len(word) > 0:
                        if word == ".":
                            flag = False
                        else:
                            if not flag:
                                if first_words_counter.has_key(word):
                                    first_words_counter[word] += 1
                                    count_dots += 1
                                else:
                                    first_words_counter[word] = 1.
                                    count_dots += 1
                                flag = True
                        words.append(word)
    return first_words_counter, words, count_dots


def create_init_distr(dict, count_dots):
    for key, value in dict.iteritems():
        dict[key] = float(value)/count_dots
    return dict


def create_stats(words):
    words.insert(0, '.')
    stats = {}
    for i in range(2, len(words)):
        temp = stats
        if not stats.has_key(words[i-2]):
            temp[words[i-2]] = {}
        temp = temp[words[i-2]]
        if not temp.has_key(words[i-1]):
            temp[words[i-1]] = {}
        temp = temp[words[i-1]]
        if not temp.has_key(words[i]):
            temp[words[i]] = 1
        else:
            temp[words[i]] += 1
    for first in stats:
        for second in stats[first]:
            sum = 0
            for third in stats[first][second]:
                sum += stats[first][second][third]
            for third in stats[first][second]:
                stats[first][second][third] = float(stats[first][second][third]) / sum
    return stats


def get_random_from_distr(distr):
    r = random.random()
    floor_prob = 0
    for word in distr:
        if floor_prob <= r <= floor_prob + distr[word]:
            return word
        floor_prob += distr[word]
    return Exception


def marcov_chain(init_dist, stats, length):
    text = []
    text.append(get_random_from_distr(init_dist))
    text.append(get_random_from_distr(stats['.'][text[0]]))
    for i in range(2, length):
        text.append(get_random_from_distr(stats[text[i-2]][text[i-1]]))
    return ' '.join(text)


first_words, words, count_dots = read_data_and_count_first_words_in_sentence()
init_dist = create_init_distr(first_words, count_dots)
stats = create_stats(words)
open('stats.txt', 'w').write(stats.__repr__())
text = marcov_chain(init_dist, stats, 10000)
open('text.txt', 'w').write(text)
