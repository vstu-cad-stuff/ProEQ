from collections import defaultdict
from itertools import product
from data import data_y
import numpy as np
import string

# find all occurrences `needle` in `haystack`
def count_overlapping_substrings(haystack, needle):
    count = 0
    i = -1
    while True:
        i = haystack.find(needle, i+1)
        if i == -1:
            return count
        count += 1

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
        for item in product(self.alphabet, repeat=product_rep):
            # normalization parameter ( result_string length )
            freq = count_overlapping_substrings(self.result_string, ''.join(item)) / result_string_len 
            self.dict_freq[item] = freq if freq > self.PROB_MIN else self.PROB_MIN
        for start in range(0, result_string_len - n_w):
            window = self.result_string[start:start + n_w]
            for left in self.alphabet:
                p = 1.0
                # compute value p(left|window)
                for right in window:
                    p *= self.dict_freq[left, right]
                self.dict_freq[left, window] = p if p > self.PROB_MIN else self.PROB_MIN

    def classify(self, sample):
        classes, prob = self.result_freq, self.dict_freq
        return min(classes.keys(),              # calculate argmin(-log(C|O))
            key = lambda cl: -np.log(classes[cl]) + \
                sum(-np.log(prob.get((cl, feat), self.PROB_MIN)) for feat in sample))

if __name__ == '__main__':
    # our parameters
    # n_s -- alphabet length
    # n_w -- window size
    n_s, n_w = 26, 5
    rep = Representer(data_y, n_w, n_s)
    res_len = len(rep.result_string)
    for window_size in range(n_w, res_len - 1):
        rep.calculate_frequence(window_size)
        M_n = 0
        n = 0
        for start in range(0, res_len - window_size, window_size - 1):
            window = rep.result_string[start:start + n_w]
            key = tuple(rep.revert(rep.result_string[start + n_w] + rep.classify(window)))
            M_n += abs((key[0] - key[1]) / key[0])
            n += 1
        M = M_n / n
        print('window = {:4}; MAPE = {:.2f}%'.format(window_size, M * 100))