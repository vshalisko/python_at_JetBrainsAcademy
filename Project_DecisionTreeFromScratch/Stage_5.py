import pandas as pd

class Node:

  def __init__(self):
    # class initialization
    self.left = None
    self.right = None
    self.term = False
    self.label = None
    self.feature = None
    self.value = None

  def set_split(self, feature, value):
    # this function saves the node splitting feature and its value
    self.feature = feature
    self.value = value

  def set_term(self, label):
    # if the node is a leaf, this function saves its label
    self.term = True
    self.label = label

class DecisionTree:

    def __init__(self):
        self.node_minimum = 1
        self.tree = Node()

    def fit(self, data, target):
        node = self.tree
        self._recursive_splitting(node, data, target)

    def predict(self, data):
        node = self.tree
        self._recursive_prediction(node, data)

    def _gini_impurity(self, D):
        # calculates GI
        D_counts = dict()
        for i in D:
            D_counts[i] = D_counts.get(i, 0) + 1
        gini_sum = 0
        for class_i in D_counts:
            p_i = D_counts[class_i] / len(D)
            gini_sum += p_i ** 2
        gini = 1 - gini_sum
        return gini

    def _weighted_gini_impurity(self, d1, d2):
        # calculates WGI
        n1 = len(d1)
        n2 = len(d2)
        n = n1 + n2
        gini1 = self._gini_impurity(d1)
        gini2 = self._gini_impurity(d2)
        return (n1 / n) * gini1 + (n2 / n) * gini2

    def _data_homogenety(self, data):
        # checks if data has the homogeneous values for each feature
        return (data.nunique() == 1).all()

    def _is_node_leaf(self, data, target):
        # checks if the current node dataset fulfills leaf criteria
        if data.shape[0] <= self.node_minimum:
            #print("len < 1")
            return True
        if self._gini_impurity(target.to_list()) == 0:
            #print("impurity = 0")
            return True
        if self._data_homogenety(data):
            #print("homogenety = True")
            return True
        return False

    def _split(self, data, target):
        # looks for the best splitting for the node
        # given dataset, by WGI
        best_feature = None
        best_value = None
        left_node = None
        right_node = None
        wgi = 1

        features = data.columns.values.tolist()
        for feature in features:
            variants = data[feature].unique()
            for value in variants:
                current_left_node = target[data[feature] == value]
                current_right_node = target[data[feature] != value]
                current_wgi = self._weighted_gini_impurity(current_left_node, current_right_node)
                if current_wgi < wgi:
                    wgi = current_wgi
                    best_feature = feature
                    best_value = value
                    left_node = current_left_node
                    right_node = current_right_node
        return wgi, best_feature, best_value, left_node.index.tolist(), right_node.index.tolist()

    def _get_label(self, target):
        # identifies the prevalent term in given target data
        variants = target.unique()
        max_counter = 0
        most_common = None
        for value in variants:
            current_count = len(target[target == value])
            if current_count > max_counter:
                max_counter = current_count
                most_common = value
        return max_counter, most_common

    def _recursive_splitting(self, tree_node, data, target):
        if self._is_node_leaf(data, target):
            # assigns label to node
            prevalence, term = self._get_label(target)
            tree_node.set_term(term)
        else:
            # generates split, two datasets and calls recursively for them
            w_gini, p_feature, p_value, left_index, right_index = self._split(data, target)
            tree_node.set_split(p_feature, p_value)
            #print(f'Made split: {tree_node.feature} is {tree_node.value}')
            tree_node.left = Node()
            left_data = data.iloc[left_index].reset_index(drop=True)
            left_target = target.iloc[left_index].reset_index(drop=True)
            self._recursive_splitting(tree_node.left, left_data, left_target)
            tree_node.right = Node()
            right_data = data.iloc[right_index].reset_index(drop=True)
            right_target = target.iloc[right_index].reset_index(drop=True)
            self._recursive_splitting(tree_node.right, right_data, right_target)

    def _recursive_prediction(self, node, data):
        if node.term:
            print(f"Predicted label: {node.label}")
            return node.label
        else:
            # print(data[node.feature])
            # print(node.left)
            print(f"Considering decision rule on feature {node.feature} with value {node.value}")
            if data[node.feature] == node.value:
                self._recursive_prediction(node.left, data)
            else:
                # print("fd'")
                self._recursive_prediction(node.right, data)

if __name__ == '__main__':
    data_paths = str(input())
    train_data_path, test_data_path = data_paths.split()
    train_data_path = "test/data_stage5_train - copia.csv"
    train_data = pd.read_csv(train_data_path, index_col=0)
    test_data_path = "test/data_stage5_test - copia.csv"
    test_data = pd.read_csv(test_data_path, index_col=0)
    #print(data)

    ## stage 1
    #D = str(input())
    #d1 = str(input())
    #d2 = str(input())
    #D = D.split()
    #d1 = d1.split()
    #d2 = d2.split()
    #print("{} {}".format(gini_impurity(D),weighted_gini_impurity(d1, d2)))

    ## stage 2
    target = train_data['Survived']
    train_data.drop(columns='Survived', inplace=True)
    #ANSWER = split(data, target)
    #for i in ANSWER:
    #    print(i, end=' ')

    ## stage 4
    dt = DecisionTree()
    dt.fit(train_data, target)

    ## stage 5
    for i in test_data.index:
        print(f"Prediction for sample # {i}")
        dt.predict(test_data.loc[i, :])
