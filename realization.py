from main import count_overlapping_substrings
from collections import defaultdict
from itertools import product
from data import data_y
import numpy as np
import string
# import nltk

PROB_MIN = 1E-300
ALPHABET = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
ALPHABET_LEN = len(ALPHABET)

def represent_data(data, n_s=len(ALPHABET)):
    if ALPHABET_LEN < n_s:
        raise('Length of alphabet is smaller that n_s')
    alpha = ALPHABET[:n_s]
    alpha_len = len(alpha) - 1
    y_min, y_max = min(data_y), max(data_y)
    y_delta = y_max - y_min
    # normalize input data and present as symbol string
    representer = lambda y: alpha[int(np.round(((y - y_min) / y_delta) * alpha_len))]
    return ''.join(map(representer, data_y)), alpha

def calc_freq(data_str, alphabet, n_w, *, product_rep=2):
    alphabet_dict = defaultdict(int)
    result_freq = defaultdict(float)
    dict_freq = defaultdict(float)
    # calc p(a) ... p(z) freq
    for item in data_str:
        alphabet_dict[item] += 1
    for k, v in alphabet_dict.items():
        result_freq[k] = v / len(data_str) if v > 0 else PROB_MIN
    # calc p(a|a), p(a|b), ..., p(b|a), ... freq
    for a, b in product(alphabet, repeat=product_rep):
        # normalization parameter ( data_str length )
        freq = count_overlapping_substrings(data_str, a + b) / len(data_str)
        dict_freq[a, b] = freq if freq > PROB_MIN else PROB_MIN
    for start in range(0, len(data_str) - n_w):
        window = data_str[start:start + n_w]
        for left in alphabet:
            p = 1.0
            # compute value p(left|window)
            for right in window:
                p *= dict_freq[left, right]
            dict_freq[left, window] = p if p > PROB_MIN else PROB_MIN
    return result_freq, dict_freq

if __name__ == '__main__':
    # our parameters
    # n_s -- alphabet length
    # n_w -- window size
    n_s, n_w = 26, 5
    res_str, alphabet = represent_data(data_y, n_s)
    prob = calc_freq(res_str, alphabet, n_w)
    # res_prob = nltk.FreqDist(res_str)