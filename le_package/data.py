
### STILL NEED TO UPLOAD THE DATA TO GCLOUD


def get_data():
    """method to get the training data (or a portion of it) from google cloud bucket"""
    client = storage.Client()
    df = pd.read_csv(
        f"gs://{BUCKET_NAME}/{BUCKET_TRAIN_DATA_PATH}", nrows=1000)
    return df
