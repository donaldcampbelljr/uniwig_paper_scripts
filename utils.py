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