import numpy as np
from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler

class CustomKMeans:
    def __init__(self, k):
        self.k = k
        self.centers = None

    def fit(self, X, eps=1e-6):
        convergence = 1
        while convergence > eps:
            labels = self.find_nearest_center(X)
            new_centers = self.calculate_new_centers(X, labels)
            convergence = self.convergence(self.centers, new_centers)
            self.centers = new_centers

    def predict(self, X):
        return self.find_nearest_center(X)

    def euclidean(self, a, b):
        ## both a & b atr numpy arrays
        squared_difference = np.square(a - b)
        return np.sqrt(np.sum(squared_difference))

    def find_nearest_center(self, X):
        distances = np.zeros((X.shape[0], self.centers.shape[0]))
        for i in range(X.shape[0]):
            for j in range(self.centers.shape[0]):
                distances[i,j] = self.euclidean(X[i,],self.centers[j,])
        return np.argmin(distances, axis=1)

    def calculate_new_centers(self, X, labels):
        levels = np.unique(labels)
        new_centers = np.zeros((len(levels), X.shape[1]))
        for level in levels:
            selector = labels == level
            new_centers[level,:] = np.mean(X[selector,:], axis=0)
        return new_centers

    def convergence(self, c1, c2):
        ## difference between centers
        convergence = np.linalg.norm(c1 - c2)
        #print(convergence)
        return convergence

    def calculate_elbow(self, X, labels):
        result = 0
        for i in range(0, X.shape[0]):
            center = self.centers[labels[i]]
            result += np.sum(np.square(X[i,] - center))
        return result

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

    inertia = []

    for k in range(2,11):
        k_model = CustomKMeans(k=k)
        if not k_model.centers:
            k_model.centers = X_full[0:k_model.k]
        k_model.fit(X_full)
        y = k_model.predict(X_full)
        inertia_score = k_model.calculate_elbow(X_full, y)
        inertia.append(inertia_score)

    cs = ', '.join(map(str, inertia))
    print(f"[{cs}]")
