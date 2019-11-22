import pandas as pd
from datetime import datetime
import pickle
import sys


def read_in(path, sep):
    '''
    convert the file into a processable object
    :param path: the file
    :param sep: separation type of each csv file
    :return: dataframe
    '''
    df = pd.read_csv(path, sep=sep, encoding = "utf-8")
    return df

def fill_statn(trp_df):
    '''
    column 'strt_statn': missing value -> replace with 0
            set type as integer
    :param trp_df: raw dataframe
    :return: revised dataframe
    '''
    trp_df['strt_statn'] = trp_df['strt_statn'].fillna(0)
    trp_df['strt_statn'] = trp_df['strt_statn'].astype('int32')
    return trp_df

def fill_gender(trp_df):
    '''
    column 'gender': missing value -> replace with 'Unknown'
    :param trp_df: unprocessed dataframe
    :return: processed dataframe
    '''
    trp_df['gender'] = trp_df['gender'].fillna('Unknown')
    return trp_df

def fill_birthyr(trp_df):
    '''
    column 'birth_date': missing value -> replace with average birth year
    :param trp_df: dataframe before processing
    :return: dataframe after processing
    '''
    mean_birthyr = round(trp_df['birth_date'].mean())
    trp_df['birth_date'] = trp_df['birth_date'].fillna(mean_birthyr)
    return trp_df

def add_age(trips_data):
    '''
    update 'age' column based on the current year and the column 'birth_date'
    assumed everyone passed their birth day
    :param trips_data: raw dataframe
    :return: updated dataframe
    '''
    cur_year = datetime.now().year
    trips_data['age'] = cur_year - trips_data['birth_date']
    return trips_data

def remove_outlier(trp_df):
    '''
    remove the outliers - here defined as the highest 5 % in 'duration'
    :param trp_df: dataframe before trimming
    :return: dataframe after trimming
    '''
    trp_df = trp_df[trp_df['duration'] <= trp_df['duration'].quantile(0.95)]
    print(trp_df[trp_df['duration'] < 0]) # minus still appears
    return trp_df

def fill_loc_statn(stn_df):
    '''
    generate datastructure to map lat/lng from station ID in trip(passenger) data
    station data has this information
    :param stn_df: station dataframe
    :return: station data
    '''
    lat_dict = dict(zip(stn_df['id'], stn_df['lat']))
    lng_dict = dict(zip(stn_df['id'], stn_df['lng']))

    return lat_dict, lng_dict

def fill_loc_trips(trips_data, lat_dict, lng_dict):
    '''
    maps lat/lng from station ID in trip data
    replace missing values with mean of the lat/lng
    :param trips_data: contains station ID
    :param lat_dict: station ID (key) - lat (val)
    :param lng_dict: station ID (key) - lng (val)
    :return: trip data with lat/lng columns
    :saves: for REST use, saves dictionary in pickle
    '''

    trips_data['lat'] = trips_data['strt_statn'].map(lat_dict)
    trips_data['lng'] = trips_data['strt_statn'].map(lng_dict)

    mean_lat = trips_data['lat'].mean()
    mean_lng = trips_data['lng'].mean()

    trips_data['lat'] = trips_data['lat'].fillna(mean_lat)
    trips_data['lng'] = trips_data['lng'].fillna(mean_lng)

    lat_dict_rest, lng_dict_rest = lat_dict, lng_dict

    # URL request purpose
    lat_dict_rest['KeyError'] = mean_lat
    lng_dict_rest['KeyError'] = mean_lng

    with open('lat_dict.p', 'wb') as out_path:
        pickle.dump(lat_dict_rest, out_path, -1)

    with open('lng_dict.p', 'wb') as out_path:
        pickle.dump(lng_dict_rest, out_path, -1)

    #sys.exit()

    return trips_data


def run(path_trp = 'data/hubway_trips.csv',
        path_stn = 'data/hubway_stations.csv'):
    '''
    main funciton of the script that calls all the preprocessing functions
    :param path_trp: trip data
    :param path_stn: station data
    :return: trip data to be used for fitting and predictting
    '''
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

    lat_dict, lng_dict = fill_loc_statn(stn_df)

    trips_data = fill_loc_trips(trips_data, lat_dict, lng_dict)

    # TODO:
    #  Integration Test: for all the new columns added
    # saving for convenience
    trips_data.to_csv('trips_data.csv', sep='\t', encoding='utf-8', mode = 'w', index=False)
    return trips_data


if __name__ =='__main__':
    _ = run()