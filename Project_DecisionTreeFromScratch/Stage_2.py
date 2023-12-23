import pandas as pd

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

def split(split_data, target_data):
    perfect_feature = None
    perfect_value = None
    left_node = None
    right_node = None
    weighted_gini_index = 1
    features = split_data.columns.values.tolist()

    for feature in features:
        kinds = split_data[feature].unique()

        for value in kinds:
            left_node_temp = target_data[split_data[feature] == value]
            right_node_temp = target_data[split_data[feature] != value]

            if weighted_gini_impurity(left_node_temp, right_node_temp) < weighted_gini_index:
                weighted_gini_index = weighted_gini_impurity(left_node_temp, right_node_temp)
                perfect_feature = feature
                perfect_value = value
                left_node = left_node_temp
                right_node = right_node_temp

    return weighted_gini_index, perfect_feature, perfect_value, left_node.index.tolist(), right_node.index.tolist()

if __name__ == '__main__':
    data_path = str(input())
    data_path = "test/data_stage2 - copia.csv"

    ## stage 1
    #D = str(input())
    #d1 = str(input())
    #d2 = str(input())
    #D = D.split()
    #d1 = d1.split()
    #d2 = d2.split()
    #print("{} {}".format(gini_impurity(D),weighted_gini_impurity(d1, d2)))

    ## srage 2
    data = pd.read_csv(data_path, index_col=0)
    target = data['Survived']
    data.drop(columns='Survived', inplace=True)
    ANSWER = split(data, target)

    for i in ANSWER:
        print(i, end=' ')
