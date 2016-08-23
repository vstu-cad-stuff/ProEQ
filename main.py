from tools import mean_absolute_error, count_overlapping_substrings
from collections import defaultdict
from data import data
from itertools import product
import numpy as np
import string

class Representer:
    PROB_MIN = 1E-300
    ALPHABET = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    ALPHABET_LEN = len(ALPHABET)

    def __init__(self, n_w, *, n_s=ALPHABET_LEN, dmin=None, dmax=None):
        if self.ALPHABET_LEN < n_s:
            raise('Length of alphabet is smaller that n_s')
        self.dmin, self.dmax = dmin, dmax
        self.alphabet = self.ALPHABET[:n_s]
        self.alpha_len = len(self.alphabet) - 1
        self.n_w = n_w

    def _represent(self, data):
        if not self.dmin:
            self.dmin = min(data)
        if not self.dmax:
            self.dmax = max(data)
        self.ddelta = self.dmax - self.dmin
        self.dstep = self.ddelta / self.alpha_len
        # normalize input data and present as symbol string
        self.representer = lambda d: \
            self.alphabet[int(np.round(((d - self.dmin) / self.ddelta) * self.alpha_len))]
        return ''.join(map(self.representer, data))

    def represent(self, data):
        return ''.join(map(self.representer, data))

    def revert(self, string):
        for item in string:
            yield self.alphabet.find(item) * self.dstep + self.dmin

    def train(self, data, *, product_rep=2):
        self.result_string = self._represent(data)
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

    def test(self, v_true, v_pred):
        hits = 0
        for true, pred in zip(v_true, v_pred):
            if true == pred:
                hits += 1
        return (hits / len(v_true)) * 100

if __name__ == '__main__':
    # our parameters
    # n_s -- alphabet length
    # n_w -- window size
    n_s, n_w = 52, 20
    dmin, dmax = min(data), max(data)
    train_data, test_data = data[:96], data[96:96 + 7 * 96]
    classifier = Representer(n_w, n_s=n_s, dmin=dmin, dmax=dmax)
    classifier.train(train_data)
    test_repr = classifier.represent(test_data)
    v_true, v_pred, l_true, l_pred = [[] for _ in range(4)]
    for x in range(len(test_repr) - 1):
        k_true = test_repr[x + 1]
        k_pred = classifier.classify(test_repr[x])
        key = tuple(classifier.revert(k_true + k_pred))
        l_true.append(k_true)
        l_pred.append(k_pred)
        # for fix 'division by zero'
        v_true.append(key[0] + 1.0)
        v_pred.append(key[1] + 1.0)
    print('alphabet = {:2}; window = {:2}; MAPE = {:6.2f}%; hits = {:6.2f}%'.format(
        n_s, n_w, mean_absolute_error(v_true, v_pred), classifier.test(l_true, l_pred)
    ))