import joblib
import pandas as pd

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sklearn.preprocessing import MinMaxScaler

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def index():
    return {"ok": "True"}


@app.get("/predict_cluster/")
def create_row(digital_transformation,
                employee_engagement,
                employee_satisfaction,
                innovation,
                internationalization,
                market_competitiveness,
                people_management,
                people_structure,
                recruitment,
                training_and_development,
                work_processes):

    # key = "2013-07-06 17:18:00.000000119"
    # pickup_datetime = "2013-07-06 17:18:00 UTC"
    # pickup_longitude = "-73.950655"
    # pickup_latitude = "40.783282"
    # dropoff_longitude = "-73.984365"
    # dropoff_latitude = "40.769802"
    # passenger_count = "1"

    # build X ⚠️ beware to the order of the parameters ⚠️
    X = pd.DataFrame(dict(
        digital_transformation=[float(digital_transformation)],
        employee_engagement=[float(employee_engagement)],
        employee_satisfaction=[float(employee_satisfaction)],
        innovation=[float(innovation)],
        internationalization=[float(internationalization)],
        market_competitiveness=[float(market_competitiveness)],
        people_management=[float(people_management)],
        people_structure=[float(people_structure)],
        recruitment=[float(recruitment)],
        training_and_development=[float(training_and_development)],
        work_processes=[float(work_processes)],

        ))
    # print("!!!!!")
    # print(digital_transformation)
    # print(X)

    # ⚠️ TODO: get model from GCP

    ## min max scaling
    X_scaled = X/5

    print(X_scaled)

    # pipeline = get_model_from_gcp()
    pipeline = joblib.load('model_le.joblib')

    print(X_scaled.dtypes)



    # make prediction
    results = pipeline.predict(X_scaled)

    # convert response from numpy to python type
    pred = float(results[0])

    return dict(
        prediction=pred)
