import joblib
from termcolor import colored
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from le_package.utils import compute_rmse
from le_package.data import get_clean_data,prepare_data
from sklearn.ensemble import VotingClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import cross_validate
import pandas as pd


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
        ### applying voting classifier to preproc
        columns = ["digital_transformation",
         "employee_engagement",
         "employee_satisfaction",
         "innovation" ,
         "internationalization",
         "market_competitiveness",
         "people_management",
         "people_structure",
         "recruitment",
         "training_and_development",
         "work_processes"]

        # pipe_prepoc = Pipeline([
        #   ('minmax',MinMaxScaler())
        #   ])

        # features_transformer = ColumnTransformer(
        #   [('ctransf',pipe_prepoc,columns)],
        #   remainder="drop")

        self.pipeline = Pipeline([
            # ('features_transformer', features_transformer),
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
        ### evaluation method for voting classifing
        #y_pred = self.pipeline.predict(self.X_test)
        ensemble_results = cross_validate(self.pipeline, self.X_train, self.y_train, cv=3)
        print("CV mean results: ", ensemble_results['test_score'].mean())
        #rmse = compute_rmse(y_pred, self.y_test)
        #return rmse

    def save_model(self):
        """Save the model into a .joblib format"""
        joblib.dump(self.pipeline, 'model_le.joblib')
        print(colored("model.joblib saved locally", "green"))

    # def save_model_to_gcp(reg):
    #     """Save the model into a .joblib and upload it on Google Storage /models folder
    #     HINTS : use sklearn.joblib (or jbolib) libraries and google-cloud-storage"""
    #     from sklearn.externals import joblib
    #     local_model_name = 'model_le.joblib'
    #     # saving the trained model to disk (which does not really make sense
    #     # if we are running this code on GCP, because then this file cannot be accessed once the code finished its execution)
    #     joblib.dump(reg, local_model_name)
    #     print("saved model.joblib locally")
    #     client = storage.Client().bucket(BUCKET_NAME)
    #     storage_location = f"models/{MODEL_NAME}/{MODEL_VERSION}/{local_model_name}"
    #     blob = client.blob(storage_location)
    #     blob.upload_from_filename(local_model_name)
    #     print("uploaded model.joblib to gcp cloud storage under \n => {}".format(
    #         storage_location))



if __name__ == "__main__":
  # get data
    df = get_clean_data()
    # clean data
    df = prepare_data(df)
    # set X and y
    # hold out
    trainer = Trainer(X=df.drop(columns="cluster"), y=df["cluster"])
    # train
    trained_model = trainer.run()
    # evaluate
    trainer.evaluate()
    trainer.save_model()
    # X = pd.DataFrame(dict(
    #     digital_transformation=[float(1)],
    #     employee_engagement=[float(1)],
    #     employee_satisfaction=[float(1)],
    #     innovation=[float(1)],
    #     internationalization=[float(1)],
    #     market_competitiveness=[float(1)],
    #     people_management=[float(1)],
    #     people_structure=[float(1)],
    #     recruitment=[float(1)],
    #     training_and_development=[float(1)],
    #     work_processes=[float(1)],

    # ))
    # print(trained_model.predict(X))
