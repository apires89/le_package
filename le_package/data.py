import pandas as pd
### STILL NEED TO UPLOAD THE DATA TO GCLOUD


def get_full_data():
    df = pd.read_csv(
        "gs://leading-enterprise-wagon-apires89/data/ecs2019_mm_ukds.csv")
    return df


def get_clean_data():
    df = pd.read_csv(
        "gs://leading-enterprise-wagon-apires89/data/final.csv")
    return df

def prepare_data(df):
    df = df.drop(columns=['sector', 'region', 'company_size'])
    df = df.astype(float)
    return df

if __name__ == "__main__":
  df = get_full_data()
  df2 = get_clean_data()
  df3 = prepare_data(df2)
  print(df3.shape)
