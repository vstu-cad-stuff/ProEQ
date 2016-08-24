import numpy as np

# find all occurrences `needle` in `haystack`
def count_overlapping_substrings(haystack, needle):
    count = 0
    i = -1
    while True:
        i = haystack.find(needle, i+1)
        if i == -1:
            return count
        count += 1

def draw_bar(min, max, current, *, size=50):
    norm = size / (max - min)
    bar = '#' * round((current - min) * norm) + '_' * round(size - (current - min) * norm)
    percent = '{:4}%'.format(round(((current - min) * norm) * (100 / size)))
    print('progress: ' + bar + percent + '\r', end='')

def calculate_errors(v_true, v_pred):
    y_true = np.asarray(v_true)
    y_pred = np.asarray(v_pred)
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    mae = np.mean(np.abs(y_true - y_pred))
    mse = np.mean(np.power(y_true - y_pred, 2))
    rmse = np.sqrt(mse)
    me = np.mean(y_true - y_pred)
    sd = np.sqrt(np.mean(np.power(y_pred - me, 2)))
    return mape, mae, mse, rmse, me, sd