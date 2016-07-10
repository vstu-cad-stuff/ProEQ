from itertools import product
from collections import defaultdict
from data import data_y, data_x
from math import log
import string
import numpy as np

# using ascii lowercase alphabet
ALPHA = string.ascii_letters
ALPHA_LEN = len(ALPHA)

# find all occurrences `needle` in `haystack`
def count_overlapping_substrings(haystack, needle):
    count = 0
    i = -1
    while True:
        i = haystack.find(needle, i+1)
        if i == -1:
            return count
        count += 1

def represent_data(data_y):
    y_min, y_max = min(data_y), max(data_y)
    # normalize the input value and the present as a symbol
    representer = lambda y: ALPHA[int(np.round(((y - y_min) / y_max) * ALPHA_LEN))]
    return ''.join(map(representer, data_y)), ALPHA

def represent_values(string, data_y):
    y_min, y_max = min(data_y), max(data_y)
    for item in string:
        yield (string.find(item) * y_max) / ALPHA_LEN + y_min


def calc_freq(data_str, alphabet):
    alphabet_dict = defaultdict(lambda:0)
    result_freq = defaultdict(lambda:0)
    dict_freq = defaultdict(lambda:0)
    # calc p(a) ... p(z) freq
    for item in data_str:
        if alphabet_dict.get(item):
            alphabet_dict[item] += 1
        else:
            alphabet_dict[item] = 1 
    for k, v in alphabet_dict.items():
        result_freq[k] = v / len(data_str)
    # calc p(a|a), p(a|b), ..., p(b|a), ... freq
    for a, b in product(alphabet, repeat=2):
        # not sure in normalization parameter ( / len(data_str) )
        count = count_overlapping_substrings(data_str, a + b) / len(data_str)
        if count > 0:
            dict_freq[a, b] = count
    return result_freq, dict_freq

def classify(classifier, feats):
    classes, prob = classifier
    return min(classes.keys(),              # calculate argmin(-log(C|O))
        key = lambda cl: -log(classes[cl]) + \
            sum(-log(prob.get((cl, feat), 10**(-7))) for feat in feats))

if __name__ == '__main__':
    # select scanning window size
    window_size = 5
    res_str, alphabet = represent_data(data_y)
    classifier = calc_freq(res_str, alphabet)
    print('Represent string = `{}`'.format(res_str))
    # compute freq for all scanning windows
    # for start in range(0, len(res_str) - window_size):
    #     window = res_str[start:start + window_size]
    #     for left in ALPHA:
    #         p = 1.0
    #         # compute value p(left|window)
    #         for right in window:
    #             p *= comb_freq[left, right]
    #         if p != 0:
    #             comb_freq[left, window] = p
    print('Classificate:')
    for start in range(0, len(res_str) - window_size, 4):
        window = res_str[start:start + window_size]
        res = classify(classifier, window)
        print('`{}` --> `{}`'.format(window, res))
    freq_list = list(classifier[1].items())
    freq_list.sort(key=lambda x: -x[1])
    print('Frequency list sorted in descending order:')
    max_field_size = int(np.round(np.log10(len(freq_list))))
    for i, item in enumerate(freq_list[:20]):
        if item[1] != 0:
            print('{index:>{max}}. p({symb}) = {value:.4e}'.format(index=i, symb=item[0], value=item[1], max=max_field_size))