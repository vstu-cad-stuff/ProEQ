#!/bin/env python3
from nltk import NaiveBayesClassifier, FreqDist
from collections import defaultdict
import numpy as np
import tools as tl
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
        for start in range(0, len(self.result_string) - self.n_w, self.n_w - 1):
            window = self.result_string[start:start + self.n_w]
            x_key = self.result_string[start + self.n_w]
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

def compute_naive_bayes(train_data, test_data, n_s, n_w, *, xstart=0, dmin=None, dmax=None):
    classifier = Representer(n_w, n_s=n_s, dmin=dmin, dmax=dmax)
    classifier.train(train_data)
    test_repr = classifier.represent(test_data)
    v_pred = []
    # for fix 'division by zero' & shift true values by one item
    v_true = list(map(lambda x: x + 1.0, test_data))[1:]
    for i, x in enumerate(range(len(test_repr) - 1)):
        k_true = test_repr[x + 1]
        k_pred = classifier.classify(test_repr[x])
        key = tuple(classifier.revert(k_pred))
        # for fix 'division by zero'
        v_pred.append(key[0] + 1.0)
    error = tl.calculate_errors(v_true, v_pred)
    v_data = list(map(lambda x: [x[0] + xstart, x[1][0], x[1][1]], enumerate(zip(v_true, v_pred))))
    return {'errors': error, 'data': [['x', 'real', 'forecast']] + v_data}