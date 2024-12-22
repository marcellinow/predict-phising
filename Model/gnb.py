import numpy as np

class NaiveBayes:
    def fit(self,X,y):
        rows,features = X.shape
        self.uniques = np.unique(y)
        n_uniques = len(self.uniques)

        self.mean = np.zeros((n_uniques, features), dtype=np.float64)
        self.var = np.zeros((n_uniques, features), dtype=np.float64)
        self.priors = np.zeros(n_uniques, dtype=np.float64)
        
        for i, unique in enumerate(self.uniques):
            X_u = X[y == unique]
            self.mean[i, :] = X_u.mean(axis=0)
            self.var[i, :] = X_u.var(axis=0)
            self.priors[i] = X_u.shape[0] / float(rows)

    def predict(self,X):
        y_pred = [self._predict(x) for x in X]
        return np.array(y_pred)
    def _predict(self,x):
        posteriors = []
        
        for idx, c in enumerate(self.uniques):
            prior = np.log(self.priors[idx])
            posterior = np.sum(np.log(self._pdf(idx, x)))
            posterior = prior + posterior
            posteriors.append(posterior)
        
        return self.uniques[np.argmax(posteriors)]
    
  
    def _pdf(self, unique_idx, x):
        mean = self.mean[unique_idx]
        var = self.var[unique_idx]
        numerator = np.exp(- (x - mean) ** 2 / (2 * var))
        denominator = np.sqrt(2 * np.pi * var)
        return numerator / denominator
 



