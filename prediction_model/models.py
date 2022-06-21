import argparse
import pickle
import time, os, sys
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split


def RMSE(pred, true):
    '''
    evaluation metric specifically written for pandas dataframe
    '''
    pred = pred.reshape(-1, 1)
    true = true.to_numpy().reshape(-1, 1)

    k = (pred- true)**2
    E = np.sqrt(k.mean())

    return E


class Model():
    '''
    Linear Regression emitting RMSE
    For efficiency, normalizing step handled in separate function.
    Then plugging into fit/predict. Skipping KFold.
    '''
    def __init__(self, df):
        self.df = df
        self.weight = []
        self.bias = 0

    def process_data(self):
        '''
        normalise: age -> min-max normalisation
                    lat, lng -> standard norm
                    gender -> one-hot encoding
        train/test split: 4 to 1
        :stores: split data
        '''
        minv = self.df['age'].max()
        maxv = self.df['age'].min()
        self.df['age'] = (self.df['age'] - minv) / (maxv - minv)

        mean = self.df['lat'].mean()
        std = self.df['lat'].std()
        self.df['lat'] = (self.df['lat'] - mean) / std
        mean = self.df['lng'].mean()
        std = self.df['lng'].std()
        self.df['lng'] = (self.df['lng'] - mean) / std

        # don't think it's a good idea, but checked that it assigns Unknown to 0 (same as male)
        # acc to some discussions online it is a more proper way to handle such situation
        print(f"{self.df['gender'].head(4)}")
        self.df['gender'].replace({'Male':0,'Unknown':0,'Female':1}, inplace=True)
        X = pd.concat([self.df['age'], self.df['lat'],
                       self.df['lng'], self.df['gender']], axis=1, sort=False)
        y = self.df['duration']

        self.X_train, self.X_test, self.y_train, self.y_test =\
                    train_test_split(X, y, test_size = 0.2, random_state = 42)

        print('Data split size in the order of:')
        print('X_train', len(self.X_train))
        print('X_test', len(self.X_test))
        print('y_train', len(self.y_train))
        print('y_test', len(self.y_test))


    def fit(self, alpha = 10):
        '''
        fitting function specific for dataframe of the given data
        while debugging, always check the shape
        :param alpha: testable regularizer
        :stores: weight and bias parameters for prediction
        :emits: RMSE
        '''
        X = np.hstack([self.X_train, np.ones((self.X_train.shape[0], 1))])
        regularI = np.sqrt(alpha) * np.identity(X.shape[1], int)

        # skip the last row so as not to regularize bias
        reg_A = np.vstack([X, regularI[:-1]])

        y = np.vstack((self.y_train[:,None], np.zeros(X.shape[1] - 1)[:, None]))

        w = np.linalg.lstsq(reg_A, y, rcond=1)[0]
        self.weight, self.bias = w[:-1], w[-1]

        pred = np.dot(self.X_train, self.weight) + self.bias
        rmse_training = RMSE(pred, self.y_train)
        print('RMSE per training data...: {}'.format(rmse_training))


    def predict(self):
        '''
        use the weight/bias params from fit function
        :param X: used for prediction
        :emits: RMSE based on test data
        '''
        print('predict', self.weight, self.weight.shape)
        print(self.X_test, self.X_test.shape)
        pred = np.dot(self.X_test, self.weight) + self.bias
        rmse_test = RMSE(pred, self.y_test)

        print('RMSE for test data...: {}'.format(rmse_test))


def main(df, filename):
    '''
    main function for linear regression training and predicting pipeline
    including saving the instance to a pickle
    :param df: dataframe retrieved from preprocess.py
    :param filename: to save the instance of the class Model
    :stores: pickle 'filename'
    '''
    linearRegressionModel = Model(df)

    toc = time.time()
    linearRegressionModel.process_data() # updates data split
    linearRegressionModel.fit()         # updates weight/bias params
    linearRegressionModel.predict()     # predicts
    tic = time.time()
    print('{}s taken..'.format(tic-toc))

    if os.path.isfile(filename):
        filename = 'model' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + '.p'

    with open(filename, 'wb') as out_path:
        pickle.dump(linearRegressionModel, out_path, -1)


def argparser():
    '''
    to run the scripts in one-liner (./run.sh shall take care of this)
    slightly hardcoded at the moment
    :return: input and output filepaths
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-tripDataPath', action='store', type = str, help='specific file on trips')
    parser.add_argument('-stationDataPath', action='store', type = str, help='specific file on stations')
    parser.add_argument('-outputPath', action='store', type = str, help='path to save the pickle')

    args = vars(parser.parse_args())

    print('check the argument parser')
    print(args)

    return args['tripDataPath'], args['stationDataPath'], args['outputPath']


if __name__ == '__main__':

    from preprocess import run

    path_trp, path_stn, output_path = argparser()

    print('trip data: ', path_trp)
    print('station data: ', path_stn)
    print('output path: ', output_path)
    # sys.exit()

    if path_trp == None or path_stn == None:
        trips_data = run()
    else:
        trips_data = run(path_trp, path_stn)

    if output_path ==None:
        filename = 'model.p'
    else:
        filename = output_path

    main(trips_data, filename)
