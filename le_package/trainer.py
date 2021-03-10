import joblib
from termcolor import colored
import mlflow
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from le_package.utils import compute_rmse
from le_package.data import get_clean_data,prepare_data
from sklearn.ensemble import VotingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier


# MLFLOW_URI = "https://mlflow.lewagon.co/"
# myname = "andrepires"
# EXPERIMENT_NAME = f"Leading_Enterprise_{myname}"


class Trainer():
    def __init__(self, X, y):
        """
            X: pandas DataFrame
            y: pandas Series
        """
        self.pipeline = None
        self.X = X
        self.y = y

    def set_pipeline(self):
        """defines the pipeline as a class attribute"""
        # instanciating different models
        #Gradient Boosting
        gradient_boost = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1
        )

        #XGBoost
        xgbc = XGBClassifier()

        #Naive Bayes Gaussian
        gaussian = GaussianNB()
        #gradient boosting
        gradient_boost_pipe = Pipeline([
            ('gradient_boost', GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1
            ))
        ])
        #creating xgbc pipeline
        xgbc_pipe = Pipeline([
            ('xgbc', XGBClassifier())
        ])
        #creating the Naive Bayes Gaussian pipeline
        gaussian_pipe = Pipeline([
            ('gaussian', GaussianNB())
        ])
        ## grouping pre voting pipeline
        preproc_pipe = Pipeline([
          ('gradient_boost',gradient_boost_pipe),
          ('xgbc',xgbc_pipe),
          ('gaussian', gaussian_pipe)
        ])
        ### applying voting classifier to preproc
        self.pipeline = Pipeline([
            ('preproc', preproc_pipe),
            ('voting_classifier', VotingClassifier(
                estimators=[("gradient_boost", gradient_boost),
                            ("xgbc", xgbc), ("gaussian", gaussian)],
                voting='soft',  # to use predict_proba of each classifier before voting
                # to equally weight forest and logreg in the vote
                weights=[2, 1, 2]
            ))
        ])
        # self.pipeline = model_pipe


    def run(self):
        self.set_pipeline()
        """set and train the pipeline"""
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, train_size=0.8)
        trained_model = self.pipeline.fit(self.X_train, self.y_train)
        return trained_model

    def evaluate(self):
        y_pred = self.pipeline.predict(self.X_train)
        rmse = compute_rmse(y_pred, self.y_train)
        return rmse


if __name__ == "__main__":
  # get data
    df = get_clean_data()
    # clean data
    prepare_data(df)
    # set X and y
    # hold out
    trainer = Trainer(X=df.drop(columns="cluster"), y=df["cluster"])
    # train
    trainer.set_pipeline()
    trainer.run()
    # evaluate
    trainer.evaluate()
    print(trainer.evaluate())
