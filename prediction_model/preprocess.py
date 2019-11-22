import pandas as pd
from datetime import datetime


def read_in(path,sep):
    # read-in
    df = pd.read_csv(path, sep=sep, encoding = "utf-8")
    return df

def fill_statn(trp_df):
    #  'strt_statn' column: missing value -> 0, set type to all as integer.
    trp_df['strt_statn'] = trp_df['strt_statn'].fillna(0)
    trp_df['strt_statn'] = trp_df['strt_statn'].astype('int32')
    return trp_df

def fill_gender(trp_df):
    #  'gender': missing -> Unknown
    trp_df['gender'] = trp_df['gender'].fillna('Unknown')
    return trp_df

def fill_birthyr(trp_df):
    #  'birth_date': missing -> average birth date?
    mean_birthyr = round(trp_df['birth_date'].mean())
    trp_df['birth_date'] = trp_df['birth_date'].fillna(mean_birthyr)
    return trp_df

def add_age(trips_data):
    #  Get and store 'age' column: from 'birth_date'
    # assuming everyone passed their birthday
    cur_year = datetime.now().year
    trips_data['age'] = cur_year - trips_data['birth_date']
    return trips_data

def remove_outlier(trp_df):
    # 'duration': remove the outliers defined as the highest 5 %
    # max value, min 0, find index with this column values < 0.95
    # then take only that
    trp_df = trp_df[trp_df['duration'] <= trp_df['duration'].quantile(0.95)]
    print(trp_df[trp_df['duration'] < 0]) # minus still appears
    return trp_df

def fill_loc_statn(stn_df):

    # to be matched with the other df for use in fitting/predicting
    lat_dict = dict(zip(stn_df['id'], stn_df['lat']))
    lng_dict = dict(zip(stn_df['id'], stn_df['lng']))

    return stn_df, lat_dict, lng_dict

def fill_loc_trips(trips_data, lat_dict, lng_dict):
    #  Get `lat`/`lng` of the `strt_statn` for each bike trip: from [stations] data
    #   If missing, use the mean of the lat/lng (processed earlier)
    trips_data['lat'] = trips_data['strt_statn'].map(lat_dict)
    trips_data['lng'] = trips_data['strt_statn'].map(lng_dict)

    mean_lat = trips_data['lat'].mean()
    mean_lng = trips_data['lng'].mean()
    trips_data['lat'] = trips_data['lat'].fillna(mean_lat)
    trips_data['lng'] = trips_data['lng'].fillna(mean_lng)

    return trips_data

# main
def run(path_trp = 'data/hubway_trips.csv',
        path_stn = 'data/hubway_stations.csv'):

    trp_df = read_in(path_trp,',')
    trp_df = fill_statn(trp_df)
    trp_df = fill_gender(trp_df)
    trp_df = fill_birthyr(trp_df)

    # TODO: from [trips] data
    #  Unit Test: On the 'duration'
    trips_data = remove_outlier(trp_df)

    trips_data = add_age(trips_data)

    # the other source
    stn_df = read_in(path_stn, ',')
    # checking because I saw no data without the corresponding information
    print(stn_df[stn_df['lat'].isnull()])
    print(stn_df[stn_df['lng'].isnull()])

    stn_df, lat_dict, lng_dict = fill_loc_statn(stn_df)
    trips_data = fill_loc_trips(trips_data, lat_dict, lng_dict)

    # TODO:
    #  Integration Test: for all the new columns added

    trips_data.to_csv('trips_data.csv', sep='\t', encoding='utf-8', mode = 'w', index=False)
    return trips_data


if __name__ =='__main__':

    _ = run()