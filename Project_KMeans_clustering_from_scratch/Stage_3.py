from cgi import print_form

import numpy as np
from sklearn.datasets import load_wine
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler

def plot_comparison(data: np.ndarray, predicted_clusters: np.ndarray, true_clusters: np.ndarray = None,
                    centers: np.ndarray = None, show: bool = True):

    # Use this function to visualize the results on Stage 6.

    if true_clusters is not None:
        plt.figure(figsize=(20, 10))

        plt.subplot(1, 2, 1)
        sns.scatterplot(x=data[:, 0], y=data[:, 1], hue=predicted_clusters, palette='deep')
        if centers is not None:
            sns.scatterplot(x=centers[:, 0], y=centers[:, 1], marker='X', color='k', s=200)
        plt.title('Predicted clusters')
        plt.xlabel('alcohol')
        plt.ylabel('malic_acid')
        plt.grid()

        plt.subplot(1, 2, 2)
        sns.scatterplot(x=data[:, 0], y=data[:, 1], hue=true_clusters, palette='deep')
        if centers is not None:
            sns.scatterplot(x=centers[:, 0], y=centers[:, 1], marker='X', color='k', s=200)
        plt.title('Ground truth')
        plt.xlabel('alcohol')
        plt.ylabel('malic_acid')
        plt.grid()
    else:
        plt.figure(figsize=(10, 10))
        sns.scatterplot(x=data[:, 0], y=data[:, 1], hue=predicted_clusters, palette='deep')
        if centers is not None:
            sns.scatterplot(x=centers[:, 0], y=centers[:, 1], marker='X', color='k', s=200)
        plt.title('Predicted clusters')
        plt.xlabel('alcohol')
        plt.ylabel('malic_acid')
        plt.grid()

    plt.savefig('Visualization.png', bbox_inches='tight')
    if show:
        plt.show()

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
        for i in range(0, X.shape[0]):
            for j in range(0, self.centers.shape[0]):
                distances[i,j] = self.euclidean(X[i,],X[j,])
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

    k_model = CustomKMeans(k=2)
    if not k_model.centers:
        k_model.centers = X_full[0:k_model.k]
    k_model.fit(X_full)

    y = k_model.predict(X_full)
    cs = ', '.join(map(str, y[:10]))
    print(f"[{cs}]")
