import joblib
from termcolor import colored
import mlflow
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from le_package.utils import compute_rmse

MLFLOW_URI = "https://mlflow.lewagon.co/"
myname = "andrepires"
EXPERIMENT_NAME = f"Leading_Enterprise_{myname}"


class Trainer():
    def __init__(self, X, y):
        """
            X: pandas DataFrame
            y: pandas Series
        """
        self.pipeline = None
        self.X = X
        self.y = y
        self.experiment_name = EXPERIMENT_NAME

    def set_pipeline(self):
        """defines the pipeline as a class attribute"""
        #creating distance pipe
        #creating time pipe
        #preprocessing
        ## chosing pipeline based on model

        # self.pipeline = model_pipe
        pass

    def run(self):
        """set and train the pipeline"""
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, train_size=0.8)
        trained_model = self.pipeline.fit(self.X_train, self.y_train)
        return trained_model

    def evaluate(self):
        y_pred = self.pipeline.predict(self.X_train)
        rmse = compute_rmse(y_pred, self.y_train)
        return rmse


# if __name__ == "__main__":
