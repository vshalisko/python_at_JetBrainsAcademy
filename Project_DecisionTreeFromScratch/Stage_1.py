def gini_impurity(D):
    D_counts = dict()
    for i in D:
        D_counts[i] = D_counts.get(i, 0) + 1

    gini_sum = 0
    for class_i in D_counts:
        p_i = D_counts[class_i] / len(D)
        gini_sum += p_i ** 2

    gini = 1 - gini_sum
    return gini

def weighted_gini_impurity(d1, d2):
    n1 = len(d1)
    n2 = len(d2)
    n = n1 + n2
    gini1 = gini_impurity(d1)
    gini2 = gini_impurity(d2)
    return (n1 / n) * gini1 + (n2 / n) * gini2

D = str(input())
d1 = str(input())
d2 = str(input())

D = D.split()
d1 = d1.split()
d2 = d2.split()

print("{} {}".format(gini_impurity(D),weighted_gini_impurity(d1, d2)))
