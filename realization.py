from main import count_overlapping_substrings
from nltk import NaiveBayesClassifier, FreqDist
from collections import defaultdict
from itertools import product
from data import data_y
import numpy as np
import string
import matplotlib.pyplot as plt

class Representer:
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
            yield self.alphabet.find(item) * self.dstep + self.dmin

    def _gen_feature(self, window, x):
        result = defaultdict(int)
        for item in window:
            result[item] = self.labels[item]
        return (result, x)

    def calculate_frequence(self, n_w):
        self.n_w = n_w
        self.labels = defaultdict(int)
        result_string_len = len(self.result_string)
        self.labels = FreqDist(self.result_string)
        train = []
        for start in range(0, len(self.result_string) - n_w, n_w - 1):
            window = self.result_string[start:start + n_w]
            x_key = self.result_string[start + n_w]
            train.append(self._gen_feature(window, x_key))
        self.classifier = NaiveBayesClassifier.train(train)

    def classify(self, sample):
        result = defaultdict(int)
        for item in sample:
            result[item] = self.labels[item]
        return self.classifier.classify(result)

def plot_bar(rep, name):
    data, bins, bins2, labels = [[] for _ in range(4)]
    for index, (label, item) in enumerate(sorted(rep.labels.items(), key=lambda x: x[0])):
        data.append(rep.labels.freq(label))
        labels.append(label)
        bins.append(index)
        bins2.append(index + 0.4)
    ax = plt.subplot(111)
    ax.bar(bins, data)
    ax.set_xticks(bins2)
    ax.set_xticklabels(labels)
    ax.grid()
    plt.xlim(min(bins), max(bins)+1)
    plt.savefig(name)

if __name__ == '__main__':
    # our parameters
    # n_s -- alphabet length
    # n_w -- window size
    n_s, n_w = 26, 2
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
