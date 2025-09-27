import numpy as np
from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler

def euclidean(a, b):
    ## both a & b atr numpy arrays
    squared_difference = np.square(a - b)
    return np.sqrt(np.sum(squared_difference))

def find_nearest_center(X, centers):
    distances = np.zeros((X.shape[0], centers.shape[0]))
    for i in range(0, X.shape[0]):
        for j in range(0, centers.shape[0]):
            distances[i,j] = euclidean(X[i,],X[j,])
    return np.argmin(distances, axis=1)

def calculate_new_centers(X, labels):
    levels = np.unique(labels)
    #print(levels)
    new_centers = np.zeros((len(levels), X.shape[1]))
    for level in levels:
        selector = labels == level
        #print(selector)
        means = np.mean(X[selector,:], axis=0)
        #print(means)
        new_centers[level,:] = means

    #print(new_centers)
    return new_centers

if __name__ == '__main__':

    # Load data
    data = load_wine(as_frame=True, return_X_y=True)
    X_full, y_full = data

    # Permutate it to make things more interesting
    rnd = np.random.RandomState(42)
    permutations = rnd.permutation(len(X_full))
    X_full = X_full.iloc[permutations]
    y_full = y_full.iloc[permutations]

    # From dataframe to ndarray
    X_full = X_full.values
    y_full = y_full.values

    # Scale data
    scaler = StandardScaler()
    X_full = scaler.fit_transform(X_full)

    centers_start = X_full[0:3,]

    y = find_nearest_center(X_full, centers_start)
    #cs = ', '.join(map(str, y[-10:]))
    #print(f"[{cs}]")

    centers_new = calculate_new_centers(X_full, y)
    centers_flatten = centers_new.flatten()
    cs = ', '.join(map(str, centers_flatten))
    print(f"[{cs}]")
