from itertools import product
from data import data_y
from string import ascii_lowercase
import numpy as np

# using ascii lowercase alphabet
ALPHA = ascii_lowercase
ALPHA_LEN = len(ALPHA)

# find all occurrences `needle` in `haystack`
def count_overlapping_substrings(haystack, needle):
    count = 0
    i = -1
    while True:
        i = haystack.find(needle, i+1)
        if i == -1:
            return count
        count += 1

def represent_data(data_y):
    y_min, y_max = min(data_y), max(data_y)
    # normalize the input value and the present as a symbol
    representer = lambda y: ALPHA[int(np.round(((y - y_min) / y_max) * ALPHA_LEN))]
    return ''.join(map(representer, data_y)), ALPHA

def calc_freq(data_str, alphabet):
    alphabet_dict = {}
    result_freq = {}
    dict_freq = {}
    # calc p(a) ... p(z) freq
    for item in data_str:
        if alphabet_dict.get(item):
            alphabet_dict[item] += 1
        else:
            alphabet_dict[item] = 1 
    for k, v in alphabet_dict.items():
        result_freq[k] = v / len(data_str)
    # calc p(a|a), p(a|b), ..., p(b|a), ... freq
    for a, b in product(alphabet, repeat=2):
        # not sure in normalization parameter ( / len(data_str) )
        dict_freq[a + '|' + b] = count_overlapping_substrings(data_str, a + b) / len(data_str)
    return result_freq, dict_freq


if __name__ == '__main__':
    # select scanning window size
    window_size = 5
    res_str, alphabet = represent_data(data_y)
    symb_freq, comb_freq = calc_freq(res_str, alphabet)
    print('Represent string = `{}`'.format(res_str))
    # compute freq for all scanning windows
    for start in range(0, len(res_str) - window_size):
        window = res_str[start:start + window_size]
        for left in ALPHA:
            p = 1.0
            # compute value p(left|window)
            for right in window:
                p *= comb_freq[left + '|' + right]
            if p != 0:
                comb_freq[left + '|' + window] = p
    with open('calculated-freq.json', 'w') as f:
        from json import dump
        dump_data = {
            'represent-string': res_str,
            'alphabet': alphabet,
            'symbol-freq': symb_freq, 
            'combination-freq': comb_freq
        }
        dump(dump_data, f)
    freq_list = list(comb_freq.items())
    freq_list.sort(key=lambda x: -x[1])
    print('Frequency list sorted in descending order:')
    max_field_size = int(np.round(np.log10(len(freq_list))))
    for i, item in enumerate(freq_list):
        if item[1] != 0:
            print('{index:>{max}}. p({symb}) = {value:.4e}'.format(index=i, symb=item[0], value=item[1], max=max_field_size))