import pandas as pd

def load_data():
    return pd.read_csv('src/database.csv')


def to_clean_time_series(df):
    datetime_index = pd.DatetimeIndex(pd.to_datetime(df['start_date']).values)
    return df.set_index(datetime_index).sort_index().drop(['zip_code', 'start_date'], axis=1)