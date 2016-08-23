from nltk import NaiveBayesClassifier, FreqDist
from tools import mean_absolute_error, count_overlapping_substrings
from collections import defaultdict
from itertools import product
from data import data
import numpy as np
import string

class Representer:
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

    def _gen_feature(self, window, x):
        result = defaultdict(int)
        for item in window:
            result[item] = self.labels[item]
        return (result, x)

    def train(self, data):
        self.result_string = self._represent(data)
        self.labels = defaultdict(int)
        result_string_len = len(self.result_string)
        self.labels = FreqDist(self.result_string)
        train = []
        for start in range(0, len(self.result_string) - n_w, n_w - 1):
            window = self.result_string[start:start + n_w]
            x_key = self.result_string[start + n_w]
            train.append(self._gen_feature(window, x_key))
        self.classifier = NaiveBayesClassifier.train(train)

    def test(self, v_true, v_pred):
        hits = 0
        for true, pred in zip(v_true, v_pred):
            if true == pred:
                hits += 1
        return (hits / len(v_true)) * 100

    def classify(self, sample):
        result = defaultdict(int)
        for item in sample:
            result[item] = self.labels[item]
        return self.classifier.classify(result)

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