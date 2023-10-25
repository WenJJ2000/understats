import csv
from matplotlib import pyplot as plt
from scipy import stats
import numpy as np
import pandas as pd


def choose_method(arr, test):
    data = excel_to_arr(arr)
    if test == "ztest":
        ans = ztest(data, 0.995, 1)
        print("this is ans : ", ans)
        write_out(ans, "output.csv")
    return ans


def excel_to_arr(f, head=None):
    vals = pd.read_excel(f, header=head).values.tolist()

    data = process_data(vals)
    write_out(vals, "input.csv")

    return data


def process_data(pd_arr):
    data = []
    for i in range(len(pd_arr[0])):
        curr = []
        for j in range(len(pd_arr)):
            curr.append(pd_arr[j][i])
        data.append(curr)
    return data


def std(arr, ddof=1):
    # ddof = 1  # degrees of freedom
    sample_sd = np.std(arr, ddof=ddof)
    return sample_sd


def write_out(arr, file):
    with open(file, "w") as f:
        write = csv.writer(f)
        write.writerow(arr)
    return


def mean(arr):
    arr = np.array(arr)
    return arr.mean()


def ztest(arr, confidence, ended):
    arr = arr[0]
    print(arr)

    n = len(arr)
    xbar = mean(arr)
    x_sd = std(arr, 1)  # sample sd
    if ended == 1:
        t_crit = stats.t.ppf(confidence, n - 1)
    else:
        a = 1 - confidence
        a = a / 2
        confidence = 1 - a
        t_crit = stats.t.ppf(confidence, n - 1)

    lower = xbar - x_sd * t_crit / np.sqrt(n)
    upper = xbar + x_sd * t_crit / np.sqrt(n)
    print(upper, lower)

    return [t_crit, lower, upper]
