import argparse
import pickle
import time, os, sys
import numpy as np
from sklearn.model_selection import train_test_split
from preprocess import * # not a good practice


def RMSE(pred, true):
    '''evaluation metric'''
    pred = pred.reshape(-1, 1)
    print('check prediction size: ', pred.shape)
    true = true.to_numpy().reshape(-1, 1)
    print('check true size: ', true.shape)

    k = (pred- true)**2
    E = np.sqrt(k.mean())

    return E


class Model():
    '''
    process_more: age -> min-max normalisation
                  lat, lng -> standard norm
                  gender -> one-hot encoding
    evaluation: RMSE
    choice: linear regression
    For time efficiency, processing handled in separate function.
    Then plugging into fit/predict. Skipping KFold.
    '''
    def __init__(self, df):
        self.df = df
        self.weight = []
        self.bias = 0

    def process_data(self):
        minv = self.df['age'].max()
        maxv = self.df['age'].min()
        self.df['age'] = (self.df['age'] - minv) / (maxv - minv)

        mean = self.df['lat'].mean()
        std = self.df['lat'].std()
        self.df['lat'] = (self.df['lat'] - mean) / std
        mean = self.df['lng'].mean()
        std = self.df['lng'].std()
        self.df['lng'] = (self.df['lng'] - mean) / std

        indexes =self.df['gender']=='Unknown'

        # uncalled for
        #self.df = self.df[self.df['gender'] != 'Unknown']
        #self.df = self.df[self.df['duration']>= 0]

        print('druation max', self.df['duration'].max())
        print('druation min', self.df['duration'].min())
        print('druation avg', self.df['duration'].mean())
        print('druation median', self.df['duration'].median())

        # don't think it's a good idea, but checked that it assigns Unknown to 0 (same as male)
        # acc to some discussions online thats a supposedly more proper way to handle
        self.df['gender'] = pd.get_dummies(self.df['gender'])

        X = pd.concat([self.df['age'], self.df['lat'],
                       self.df['lng'], self.df['gender']], axis=1, sort=False)
        y = self.df['duration']

        self.X_train, self.X_test, self.y_train, self.y_test =\
                    train_test_split(X, y, test_size = 0.2, random_state = 42)

       # print('length of training data size', len(self.X_train), len(self.y_train)) 1200176
       # print('length of test data size', len(self.X_test), len(self.y_test)) 300045
       # print('index check for training data\n', self.X_train, '\n', self.y_train)
       # print('index check for test data\n', self.X_test,'\n', self.y_test)


    def fit(self, alpha = 10):
        '''
        input: Training data (0.8)
        '''
        X = np.hstack([self.X_train, np.ones((self.X_train.shape[0], 1))])
        print('check buffed X shape')
        print(X.shape)
        regularI = np.sqrt(alpha) * np.identity(X.shape[1], int)

        # skip the last row so as not to regularize bias
        reg_A = np.vstack([X, regularI[:-1]])
        print('check regularizer shape')
        print(reg_A.shape)

        print('y-------------------------------------------------------')
        print(len(self.y_train),'\n',self.y_train)
        print('X-------------------------------------------------------')
        print(X.shape, '\n', X)
        y = np.vstack((self.y_train[:,None], np.zeros(X.shape[1] - 1)[:, None]))
        print('check again: ',y.shape)

        w = np.linalg.lstsq(reg_A, y, rcond=1)[0]
        print('what? weight shape?', w.shape)
        print('weight',w[:-1])
        print('bias', w[-1])
        self.weight, self.bias = w[:-1], w[-1]
        pred = np.dot(self.X_train, self.weight) + self.bias
        rmse_training = RMSE(pred, self.y_train)
        print('RMSE per training data...: {}'.format(rmse_training))


    def predict(self):
        '''
        input: age, lat, lng, gender - Test data
        use the weight params from fit process using training data
        '''
        pred = np.dot(self.X_test, self.weight) + self.bias
        rmse_test = RMSE(pred, self.y_test)
        print('RMSE for test data...: {}'.format(rmse_test))

    # TODO:
    #  docstrings, log messages throughout the code


def main(df, filename):

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

    parser = argparse.ArgumentParser()
    parser.add_argument('-tripDataPath', action='store', type = str, help='specific file on trips')
    parser.add_argument('-stationDataPath', action='store', type = str, help='specific file on stations')
    parser.add_argument('-outputPath', action='store', type = str, help='path to save the pickle')

    args = vars(parser.parse_args())

    print('check the argument parser')
    print(args)

    return args['tripDataPath'], args['stationDataPath'], args['outputPath']


if __name__ == '__main__':

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
