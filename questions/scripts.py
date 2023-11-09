import csv
from matplotlib import pyplot as plt
from scipy import stats
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
import json


def excel_to_arr(f, head=None):
    # print(type(f.name), type(f))
    vals = []
    # print(str(f), str(f).endswith(".xlx"), str(f).endswith(".csv"))
    if str(f).endswith(".xlsx"):
        vals = pd.read_excel(f, header=head).values.tolist()
    elif str(f).endswith(".csv"):
        vals = pd.read_csv(f).values.tolist()

    # print(vals)
    data = process_data(vals)
    write_out(vals, "input.csv")
    # print(data)
    return data


def process_data(pd_arr):
    if not pd_arr:
        return pd_arr
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


def write_out_json(dic, file):
    with open(file, "w") as f:
        json_obj = json.dumps(dic)
        f.write(json_obj)
    return


def mean(arr):
    arr = np.array(arr)
    return arr.mean()


def ztest(data, confidence, ended):
    arr = data
    arr = arr[0]
    # print(arr)

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
    # print(upper, lower)

    return {"t_crit": t_crit, "lower_limit": lower, "upper_limit": upper}


def simple_linear_regression(data, confidence, ended):
    # print(data)
    X_train = np.array(data[0]).reshape((-1, 1))
    y_train = np.array(data[1])
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    return {
        "coefficient_of_determination": lr.score(X_train, y_train),
        "intercept": lr.intercept_,
    }


def one_sample_chi_sq_test_for_variances(data, confidence, ended):
    return


def chi_sq_test(data, confidence, ended):
    return


def one_way_ANOVA(data, confidence, ended):
    return


def two_way_ANOVA(data, confidence, ended):
    return


def one_sample_t_test(data, confidence, ended):
    return


def paired_t_test(data, confidence, ended):
    return


def one_sample_possion_test(data, confidence, ended):
    return


mp = {
    "ztest": lambda data: ztest(**data),
    "simple_linear_regression": lambda data: simple_linear_regression(**data),
    "one_sample_chi_sq_test_for_variances": lambda data: one_sample_chi_sq_test_for_variances(
        **data
    ),
    "chi_sq_test": lambda data: chi_sq_test(**data),
    "one_way_anova": lambda data: one_way_ANOVA(**data),
    "two_way_anova": lambda data: two_way_ANOVA(**data),
    "one_sample_t_test": lambda data: one_sample_t_test(**data),
    "paired_t_test": lambda data: paired_t_test(**data),
    "one_sample_possion": lambda data: one_sample_possion_test(**data),
}


def choose_method(excel, test, confidence):
    data = excel_to_arr(excel)
    fn = mp.get(test, None)
    if fn is None:
        return None
    ans = fn({"data": data, "confidence": confidence, "ended": 1})
    print("this is ans : ", ans)
    write_out_json(ans, "output.json")
    return ans
