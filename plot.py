from os.path import splitext, join
import matplotlib.pyplot as plt
from tools import draw_bar
from os import listdir
import numpy as np
import json as js
import re

regex = re.compile('\d+')
PATH = 'data'

def read_json(filename):
    data = None
    with open(filename, 'r') as fp:
        data = js.load(fp)
    return data

if __name__ == '__main__':
    files = list(filter(lambda x: splitext(x)[1] == '.json', listdir(PATH)))
    files_count = len(files)
    for index, file in enumerate(files):
        raw_data = read_json(join(PATH, file))
        n_s, n_w = map(lambda x: regex.search(x).group(0), splitext(file)[0].split('-'))
        x_data = np.arange(len(raw_data['value_true']))
        y_true = np.asarray(raw_data['value_true'])
        y_pred = np.asarray(raw_data['value_pred'])
        f, ax = plt.subplots(2, sharex=True)
        ax[0].plot(x_data, y_true, '-g')
        ax[0].plot(x_data, y_pred, '-b')
        lgd1 = ax[0].legend(('true', 'predict'), loc='center left', bbox_to_anchor=(1, 0.86), fancybox=True, shadow=True)
        ax[0].set_title('alphabet = {}, window = {}'.format(n_s, n_w))
        ax[0].grid()
        ax[1].plot(x_data, y_pred - y_true, '-r')
        lgd2 = ax[1].legend(('error',), loc='center left', bbox_to_anchor=(1, 0.92), fancybox=True, shadow=True)
        ax[1].set_title('Absolute error')
        ax[1].grid()
        plt.savefig('data/alph{}-window{}.png'.format(n_s, n_w), dpi=300, bbox_extra_artists=(lgd1, lgd2), bbox_inches='tight')
        plt.close()
        draw_bar(0, files_count, index)