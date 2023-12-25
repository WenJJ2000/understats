import csv
from matplotlib import pyplot as plt
from scipy import stats
from statsmodels.stats.contingency_tables import mcnemar
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


def ztest(data, confidence, ended, stat):
    arr = data
    arr = arr[0]
    # print(arr)

    n = len(arr)
    xbar = mean(arr)
    x_sd = std(arr, 1)  # sample sd
    z = (xbar - stat) / (x_sd / np.sqrt(n))

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

    return {"t_crit": t_crit, "z_stat": z, "lower_limit": lower, "upper_limit": upper}


def simple_linear_regression(data, confidence, ended, stat):
    # print(data)
    X_train = np.array(data[0]).reshape((-1, 1))
    y_train = np.array(data[1])
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    return {
        "coefficient_of_determination": lr.score(X_train, y_train),
        "intercept": lr.intercept_,
    }


def one_sample_chi_sq_test_for_variances(data, confidence, ended, stat):
    arr = data[0]
    n = len(arr)
    alpha = 1 - confidence
    q = (n - 1) * np.var(arr) / stat
    if ended == 1:
        lower = stats.chi2.ppf(alpha, n - 1)
        upper = stats.chi2.ppf(confidence, n - 1)
    else:
        lower = stats.chi2.ppf(alpha / 2, n - 1)
        upper = stats.chi2.ppf(1 - (alpha / 2), n - 1)

    p = stats.chi2.cdf(q, n - 1)

    return {"Lower": lower, "Upper": upper, "Test_stat": q, "p-value": p}


def bionomial_normal_theory_test(data, confidence, ended, stat):
    arr = np.array(data[0])
    n = len(data[0])
    p0 = sum(arr) / n

    z = (p0 - stat) / (np.sqrt(p0 * (1 - p0) / n))
    if ended == 1:
        a = 1 - confidence
        lower = stats.norm.ppf(a)
        upper = stats.norm.ppf(1 - a)
    if ended == 2:
        a = 1 - confidence
        a = a / 2
        lower = stats.norm.ppf(a)
        upper = stats.norm.ppf(1 - a)

    p = stats.norm.cdf(z, n - 1)

    return {"Lower": lower, "Upper": upper, "Test_stat": z, "p-value": p}


def bionomial_exact_method_test(data, confidence, ended, stat):
    arr = np.array(data[0])
    n = len(data[0])
    p0 = sum(arr) / n
    p = 0
    if p0 <= stat:
        for i in range(n - 1):
            bi = stats.binom.pmf(i, n, p0)
            if bi <= stat:
                p += bi
    elif p0 > stat:
        for i in range(n - 1):
            bi = stats.binom.pmf(i, n, p0)
            if bi > stat:
                p += bi
    return {"p-value": p}


def one_sample_possion_test(data, confidence, ended, stat):
    arr = np.array(data[0])
    x = mean(arr)
    u0 = sum(arr)
    # need more input fields, to do
    return {"test": "to be implemented"}


def signed_rank_test(data, confidence, ended, stat):
    arr = np.array(data[0])
    narr = np.array()
    for i in arr:
        narr[i] = abs(arr[i] - stat)
    n = arr.size
    # E = n(n / 1) / 4
    # var = n * (n + 1) * (2 * n + 1) / 24
    rank, pval = stats.wilcoxon(arr - stat, zero_method="wilcox", correction=False)
    return {"rank": rank, "p-value": pval}


def two_sample_F_test(data, confidence, ended, stat):
    arr1 = np.array(data[0])
    arr2 = np.array(data[1])
    var1 = np.var(arr1, ddof=1)
    var2 = np.var(arr2, ddof=1)
    f_val = var1 / var2
    df1 = len(arr1) - 1
    df2 = len(arr2) - 1
    p_value = stats.f.cdf(f_val, df1, df2)

    return {"p_value": p_value, "df1": df1, "df2": df2}


def paired_t_test(data, confidence, ended, stat):
    arr1 = np.array(data[0])
    arr2 = np.array(data[1])
    t, p_val = stats.ttest_rel(arr1, arr2)
    return {"test_stat": t, "p_value": p_val}


def two_sample_t_eq_var(data, confidence, ended, stat):
    arr1 = np.array(data[0])
    arr2 = np.array(data[1])
    # n1, n2 = arr1.size, arr2.size
    # x1, x2 = mean(arr1), mean(arr2)
    # var1 = np.var(arr1, ddof=1)
    # var2 = np.var(arr2, ddof=1)

    # s = np.sqrt(((n1 - 1) * var1**2 + (n2 - 1) * var2**2) / (n1 + n2 - 2))

    # t = (x1 - x2) / (s * ((1 / n1) + (1 / n2)))
    t, p_val = stats.ttest_ind(a=arr1, b=arr2, equal_var=True)
    return {"test_stat": t, "p_value": p_val}


def two_sample_t_uneq_var(data, confidence, ended, stat):
    arr1 = np.array(data[0])
    arr2 = np.array(data[1])
    # var1 = np.var(arr1, ddof=1)
    # var2 = np.var(arr2, ddof=1)

    t, p_val = stats.ttest_ind(a=arr1, b=arr2, equal_var=False)
    return {"test_stat": t, "p_value": p_val}


def mcnemar_test(data, confidence, ended, stat):
    arr = []
    for col in range(data[0]):
        curr = []
        for row in range(data):
            curr.append(data[row][col])
        arr.append(curr)
    p1, stat1, p2, stat2 = mcnemar(arr, exact=False, correction=False)
    return {
        "p_value 1 ": p1,
        "test stat 1": stat1,
        "p_value 2": p2,
        "test stat 2": stat2,
    }


def fishers_exact_test(data, confidence, ended, stat):
    arr = []
    for col in range(data[0]):
        curr = []
        for row in range(data):
            curr.append(data[row][col])
        arr.append(curr)
    odd_ratio, p_value = stats.fisher_exact(data)
    return {"odd ration": odd_ratio, "P-value": p_value}


def wilcoxon_rank_test(data, confidence, ended, stat):
    arr1 = np.array(data[0])
    arr2 = np.array(data[1])

    test_stat, p_value = stats.wilcoxon(arr1, arr2)

    return {"test stats": test_stat, "p-value": p_value}


def sum_sq_mat(table):
    rows = []
    cols = []
    for i in range(len(table)):
        rows.append(sum(table[i, :]))
    for i in range(len(table[0])):
        cols.append(sum(table[:, i]))
    return [rows, cols]


def exp_mat(table):
    rows, cols = sum_sq_mat(table)
    t_row = sum(rows)
    exp_mat = []
    for i in range(len(rows)):
        row = []
        for j in range(len(cols)):
            row.append(rows[i] * (cols[j] / t_row))
        exp_mat.append(row)
    return exp_mat


def chi_sq_test(data, confidence, ended, stat):  # parse in Frequency array
    table = data
    expmat = exp_mat(data)
    chi_sq_stat = 0
    for i in range(len(table)):
        for j in range(len(table[0])):
            chi_sq_stat += (np.abs(table[i][j] - expmat[i][j])) ** 2 / expmat[i][j]
    ddof = (len(table) - 1) * (len(table[0]) - 1)
    chi_crit = stats.chi2.ppf(confidence, ddof)

    p_value = 1 - stats.chi2.cdf(chi_sq_stat, ddof)

    return {"chi sq stat": chi_sq_stat, "chi crit": chi_crit, "p_value": p_value}


def ANOVA(data, confidence, ended, stat):
    arr = data
    xbars = [mean(i) for i in arr]
    sd = [std(i, 1) for i in arr]
    var = [i**2 for i in sd]
    s_wit = np.sum(var) / len(arr)
    t_mean = np.sum(xbars) / len(arr)
    s_bet = 0
    for i in range(len(arr)):
        curr = arr[i]
        s_bet += (xbars[i] - t_mean) ** 2
    s_bet = s_bet / (len(arr) - 1)
    s_bet = s_bet * len(arr[0])

    f_ratio = s_bet / s_wit
    alpha = 1 - confidence
    dfn = len(arr) - 1  # numerator dof = m-1
    dfd = len(arr) * (len(arr[0]) - 1)  # denominator dof = m*(n-1)
    f_crit = stats.f.ppf(1 - alpha, dfn, dfd)
    p_value = 1 - stats.f.cdf(f_ratio, dfn, dfd)
    result = "Reject null" if f_ratio > f_crit else "Cannot reject null"
    return {"p Value": p_value, "f ratio": f_ratio, "f crit": f_crit, "result": result}


def one_sample_t_test(data, confidence, ended, stat):
    arr = data[0]
    n = len(arr)
    xbar = arr.mean()
    x_sd = std(arr, 1)
    x1 = stat
    t_stat = (xbar - x1) / (x_sd / np.sqrt(n))
    ddof = n - 1
    if ended == 1:
        t_crit = stats.t.ppf(confidence, n - 1)
    else:
        a = 1 - confidence
        a = a / 2
        confidence = 1 - a
        t_crit = stats.t.ppf(confidence, n - 1)
    result = "Rejected null " if np.abs(t_stat) > t_crit else "null not rejected"
    p_value = 2 * (1 - stats.t.cdf(np.abs(t_stat), ddof))

    return {"p - vlaue": p_value, "T stat": t_stat, "T crit": t_crit, "result": result}


def rank_correlation_method(data, confidence, ended, stat):
    return


def person_correlation(data, confidence, ended, stat):
    return


def kruskal_wallis_test(data, confidence, ended, stat):
    return


def contingency_table(data, confidence, ended, stat):
    return


def kappa_statistic(data, confidence, ended, stat):
    return


def multiple_regression(data, confidnce, ended, stat):
    return


def multiple_log_regression(data, confidnce, ended, stat):
    return


def one_sample_incidence_test(data, confidnce, ended, stat):
    return


def log_rank_test(data, confidnce, ended, stat):
    return


mp = {
    "ztest": lambda data: ztest(**data),
    "simple_linear_regression": lambda data: simple_linear_regression(**data),
    "one_sample_chi_sq_test_for_variances": lambda data: one_sample_chi_sq_test_for_variances(
        **data
    ),
    "bionomial_normal_theory_test": lambda data: bionomial_normal_theory_test(**data),
    "Exact_Methods": lambda data: bionomial_exact_method_test(**data),
    "signed_rank_test": lambda data: signed_rank_test(**data),
    "two_sample_F_test": lambda data: two_sample_F_test(**data),
    "paired_t_test": lambda data: paired_t_test(**data),
    "two_sample_t_eq_var": lambda data: two_sample_t_eq_var(**data),
    "two_sample_t_uneq_var": lambda data: two_sample_t_uneq_var(**data),
    "mcnemar_test": lambda data: mcnemar_test(**data),
    "fishers_exact_test": lambda data: fishers_exact_test(**data),
    "wilcoxon_rank_test": lambda data: wilcoxon_rank_test(**data),
    "chi_sq_test": lambda data: chi_sq_test(**data),
    "one_way_anova": lambda data: ANOVA(**data),
    "two_way_anova": lambda data: ANOVA(**data),
    "one_sample_t_test": lambda data: one_sample_t_test(**data),
    "one_sample_possion": lambda data: one_sample_possion_test(**data),
    #
    #
    #
    "rank_correlation_methods": lambda data: rank_correlation_method(**data),
    "person_correlation": lambda data: person_correlation(**data),
    "kruskal_wallis_test": lambda data: kruskal_wallis_test(**data),
    "contingency_table": lambda data: contingency_table(**data),
    "kappa_statistic": lambda data: kappa_statistic(**data),
    "multiple_regression": lambda data: multiple_regression(**data),
    "multiple_log_regression": lambda data: multiple_log_regression(**data),
    "one_sample_incidence_test": lambda data: one_sample_incidence_test(**data),
    "log_rank_test": lambda data: log_rank_test(**data),
}


def choose_method(excel, test, confidence, stat, ended):
    data = excel_to_arr(excel)
    fn = mp.get(test, None)
    if fn is None:
        return None
    ans = fn({"data": data, "confidence": confidence, "ended": ended, "stat": stat})
    print("this is ans : ", ans)
    write_out_json(ans, "output.json")
    return ans
