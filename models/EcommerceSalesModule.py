import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


class EcommerceSalesModule:
    def __init__(self):
        self.model = LinearRegression()

    def train(self, X, y):
        self.model.fit(X, y)
        return self

    def predict(self, X):
        return self.model.predict(X)

    @staticmethod
    def evaluate(y_true, y_pred):
        return {
            "Mean Absolute Error": mean_absolute_error(y_true, y_pred),
            "Root Mean Squared Error": np.sqrt(
                mean_squared_error(y_true, y_pred)
            ),
            "R-squared": r2_score(y_true, y_pred),
        }
