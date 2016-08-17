# http://stevenloria.com/how-to-build-a-text-classification-system-with-python-and-textblob/
from collections import defaultdict
from main import represent_data
from itertools import product
from data import data_y
import nltk

def gen_feature(window, x, labels):
    result = defaultdict(int)
    for item in window:
        result[item] = labels[item]
    return [result, x]

def classify(string, classifier, labels):
    result = defaultdict(int)
    for item in string:
        result[item] = labels[item]
    return classifier.classify(result)

if __name__ == '__main__':
    res_str, alphabet = represent_data(data_y)
    max_window_size = len(res_str) // 3
    print('Represent string = `{}`'.format(res_str))
    labels = nltk.FreqDist(res_str)
    # print(labels.most_common())
    train = []
    for window_size in range(2, max_window_size):
        for start in range(0, len(res_str) - window_size, window_size-1):
            window = res_str[start:start + window_size]
            x_key = res_str[start + window_size]
            train.append(gen_feature(window, x_key, labels))
    classifier = nltk.NaiveBayesClassifier.train(train)
    # string = res_str[-10:]
    string = 'ljgec'
    print('classify(`{}`) --> `{}`'.format(string, classify(string, classifier, labels)))
    print(classifier.most_informative_features())