import pandas as pd

def f_beta_score(beta,tp,fp,fn):
    # tp = a = the number of attributes that equal 1 for both objects i and j
    # fp = b = the number of attributes that equal 0 for object i but equal 1 for object j
    # fn = c = the number of attributes that equal 1 for object i but equal 0 for object j
    # d = the number of attributes that equal 0 for both objects i and j but we do not need to consider these.

    precision = tp/(tp+fp)
    recall = tp/(tp+fn)

    try:
        f_beta = ((1+beta**2)*precision*recall)/(((beta**2)*precision)+recall)
    except ZeroDivisionError:
        f_beta = 0

    return f_beta


def get_recall(tp,fn):
    recall = tp/(tp+fn)
    return recall

def get_precision(tp, fp):
    precision = tp/(tp+fp)
    return precision



# Helper funcs from geniml

def get_rbs(f_t_u, u_t_f):
    """
    Calculate RBS
    """
    a = 101 / (f_t_u + 100)
    b = 101 / (u_t_f + 100)
    rbs = (10 * a + b) / 11
    return rbs

def get_rbs_from_assessment_file(file, cs_each_file=False, flexible=False):
    """
    Calculate RBS form file with results of metrics per file
    :param str file: path to file with assessment results
    :param bool cs_each_file: if report RBS for each file, not average for the collection
    :param bool flexible: if use flexible version of the metric
    """
    df = pd.read_csv(file, index_col=(0))
    if flexible:
        df["f_t_u"] = df["median_dist_file_to_universe_flex"]
        df["u_t_f"] = df["median_dist_universe_to_file_flex"]
    else:
        df["f_t_u"] = df["median_dist_file_to_universe"]
        df["u_t_f"] = df["median_dist_universe_to_file"]
    df["RBS"] = get_rbs(df["f_t_u"], df["u_t_f"])
    if cs_each_file:
        return df
    else:
        return df["RBS"].mean()
    

def get_f_10_score_from_assessment_file(file, f10_each_file=False):
    """
    Get F10 score from assessment output file
    :param str file: path to file with assessment results
    :param bool f10_each_file: if report F10 for each file, not average for the collection
    """
    df = pd.read_csv(file, index_col=(0))
    r = df["universe&file"] / (df["universe&file"] + df["file/universe"])
    p = df["universe&file"] / (df["universe&file"] + df["univers/file"])
    df["F_10"] = (1 + 10**2) * (p * r) / ((10**2 * p) + r)
    if f10_each_file:
        return df["F_10"]
    else:
        return df["F_10"].mean()