from main import count_overlapping_substrings
from collections import defaultdict
from itertools import product
from data import data_y
import numpy as np
import string
# import nltk

class Representer:
    PROB_MIN = 1E-300
    ALPHABET = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    ALPHABET_LEN = len(ALPHABET)

    def __init__(self, data, n_w, n_s=ALPHABET_LEN):
        if self.ALPHABET_LEN < n_s:
            raise('Length of alphabet is smaller that n_s')
        self.data = data
        self.alphabet = self.ALPHABET[:n_s]
        self.alpha_len = len(self.alphabet) - 1
        self.result_string = self.represent(data)
        self.calculate_frequence(n_w)

    def __iadd__(self, new_data):
        if type(new_data) not in (list, tuple):
            raise('Type is not supported')
        self.result_string += self.represent(new_data)
        self.calculate_frequence(self.n_w)

    def __isub__(self, substring):
        if type(other) is not str:
            raise('Type is not supported')
        self.result_string.replace(substring, '')
        self.calculate_frequence(self.n_w)

    def represent(self, data):
        self.data += data
        self.dmin, self.dmax = min(self.data), max(self.data)
        self.ddelta = self.dmax - self.dmin
        self.dstep = self.ddelta / self.alpha_len
        # normalize input data and present as symbol string
        self.representer = lambda d: \
            self.alphabet[int(np.round(((d - self.dmin) / self.ddelta) * self.alpha_len))]
        return ''.join(map(self.representer, self.data))

    def revert(self, string):
        for item in string:
            yield string.find(item) * self.dstep + self.dmin

    def calculate_frequence(self, n_w, *, product_rep=2):
        self.n_w = n_w
        alphabet_dict = defaultdict(int)
        self.result_freq = defaultdict(float)
        self.dict_freq = defaultdict(float)
        result_string_len = len(self.result_string)
        # calc p(a) ... p(z) freq
        for item in self.result_string:
            alphabet_dict[item] += 1
        for k, v in alphabet_dict.items():
            self.result_freq[k] = v / result_string_len if v > 0 else self.PROB_MIN
        # calc p(a|a), p(a|b), ..., p(b|a), ... freq
        for a, b in product(self.alphabet, repeat=product_rep):
            # normalization parameter ( result_string length )
            freq = count_overlapping_substrings(self.result_string, a + b) / result_string_len 
            self.dict_freq[a, b] = freq if freq > self.PROB_MIN else self.PROB_MIN
        for start in range(0, result_string_len - n_w):
            window = self.result_string[start:start + n_w]
            for left in self.alphabet:
                p = 1.0
                # compute value p(left|window)
                for right in window:
                    p *= self.dict_freq[left, right]
                self.dict_freq[left, window] = p if p > self.PROB_MIN else self.PROB_MIN

if __name__ == '__main__':
    # our parameters
    # n_s -- alphabet length
    # n_w -- window size
    n_s, n_w = 26, 5
    rep = Representer(data_y, n_w, n_s)