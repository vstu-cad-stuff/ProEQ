from nltk import NaiveBayesClassifier, FreqDist
from collections import defaultdict
from itertools import product
from data import data
import tools as tl
import numpy as np
import json as js
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

def select_train_data(data, *, window=96, feature_size=None):
    train_data = None
    remove_index = 0
    sigma = 0
    for index in range(0, len(data), window):
        day = data[index:index + window]
        curr_sigma = np.std(day)
        if curr_sigma > sigma:
            remove_index = index
            train_data = day
    data = data[0:index] + data[index + window:]
    if feature_size:
        return train_data, data[:feature_size]
    else:
        return train_data, data

def compute_naive_bayes(train_data, test_data, n_s, n_w, *, dmin=None, dmax=None):
    classifier = Representer(n_w, n_s=n_s, dmin=dmin, dmax=dmax)
    classifier.train(train_data)
    test_repr = classifier.represent(test_data)
    v_pred, l_true, l_pred = [[] for _ in range(3)]
    # for fix 'division by zero' & shift true values by one item
    v_true = list(map(lambda x: x + 1.0, test_data[1:]))
    for x in range(len(test_repr) - 1):
        k_true = test_repr[x + 1]
        k_pred = classifier.classify(test_repr[x])
        key = tuple(classifier.revert(k_pred))
        l_true.append(k_true)
        l_pred.append(k_pred)
        # for fix 'division by zero'
        v_pred.append(key[0] + 1.0)
    errors = tl.calculate_errors(v_true, v_pred)
    hits = classifier.test(l_true, l_pred)
    return errors[3]

if __name__ == '__main__':
    # skip 31 days and take 1 train and 7 testing days
    data = data[31 * 96:(31 + 8) * 96]
    dmin, dmax = min(data), max(data)
    train_data, test_data = select_train_data(data)
    alpha_range = (4, Representer.ALPHABET_LEN)
    window_range = (2, Representer.ALPHABET_LEN)
    n_s, n_w = alpha_range[0], window_range[0]
    alph_index, wind_index, delta_index = 0, 0, 5
    fit_value = compute_naive_bayes(train_data, test_data, n_s, n_w, dmin=dmin, dmax=dmax)
    print('[start] alphabet = {}; window = {}; fit function = {:6.2f}'.format(n_s, n_w, fit_value))
    for s_index, new_s in enumerate(range(alpha_range[0], alpha_range[1])):
        for w_index, new_w in enumerate(range(window_range[0], window_range[1])):
            new_value = compute_naive_bayes(train_data, test_data, new_s, new_w, dmin=dmin, dmax=dmax)
            if new_value < fit_value:
                n_s, n_w, fit_value = new_s, new_w, new_value
                alph_index, wind_index = s_index, w_index
            elif w_index - wind_index > delta_index:
                break
            print('[{}, {}] alphabet = {}; window = {}; fit function = {:6.2f}'.format(
                s_index, w_index, new_s, new_w, new_value
            ))
        if s_index - alph_index > delta_index:
            break
    print('[best] alphabet = {}; window = {}; fit function = {:6.2f}'.format(n_s, n_w, fit_value))