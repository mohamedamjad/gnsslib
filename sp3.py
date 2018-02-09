#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR


class Sp3(object):
    """The Sp3 module

    The Sp3 module deals with the SP3 () file format
    """
    def __init__(self):
        """initiate the Sp3 module"""
        self.version_symbol = ""
        self.pos_or_vel = ""
        self.year_start = 0
        self.month_start = 0
        self.day_start = 0
        self.hour_start = 0
        self.minute_start = 0
        self.second_start = 0.0
        self.number_of_epochs = 0
        self.data_used = ""
        self.coordinate_sys = ""
        self.orbit_type = ""
        self.agency = ""
        self.gps_week = 0
        self.seconds_of_week = 0.0
        self.epoch_interval = 0.0
        self.julian_day = 0
        self.fractional_day = 0.0
        self.number_of_sats = 0.0
        self.dataset = pd.DataFrame()
        self.x_model_coeffs = []
        self.y_model_coeffs = []
        self.z_model_coeffs = []

    def parse(self, sp3_file_path):
        tmp_list = []
        with open(sp3_file_path) as fp:
            for line in fp:
                if '*  ' in line:
                    date_time = line.split()[1:len(line.split())]
                    line = fp.next()
                    while '*  ' not in line:
                        date_time_string = pd.to_datetime(date_time[2] + '-' +
                                                          date_time[1] + '-' +
                                                          date_time[0] + ' ' +
                                                          date_time[3] + ':' +
                                                          date_time[4] + ':' +
                                                          date_time[5])
                        new_row = [date_time_string, line[0], line[1:4],
                                   float(line[4:18]), float(line[18:32]),
                                   float(line[32:46]),
                                   float(line[46:60]), line[61:63],
                                   line[64:66], float(line[67:69]),
                                   line[70:73], line[74], line[75],
                                   line[78], line[79]]
                        tmp_list.append(new_row)
                        line = fp.next()
        self.dataset = pd.DataFrame(tmp_list, columns=['date_time', 'type',
                                                       'PRN', 'x',
                                                       'y', 'z', 'clock',
                                                       'x_sdev', 'y_sdev',
                                                       'z_sdev', 'c_sdev',
                                                       'clk_event_flag',
                                                       'clk_pred_flag',
                                                       'manoeuvre_flag',
                                                       'orb_predict_flag'])
        self.dataset['unix_time'] = sp3.dataset['date_time'].values.\
                                    astype(np.int64)/1000000000

    def fit(self):
        """fit the model"""

        # Prepare the data
        timestamp = self.dataset['unix_time'].as_matrix().reshape(-1,1)
        x = self.dataset['x'].as_matrix().reshape(-1,1)
        y = self.dataset['y'].as_matrix().reshape(-1,1)
        z = self.dataset['z'].as_matrix().reshape(-1,1)

        # Scale the features and targets
        ss_timestamp = StandardScaler()
        timestamp = ss_timestamp.fit_transform(timestamp)

        ss_x = StandardScaler()
        x = ss_x.fit_transform(x)

        ss_y = StandardScaler()
        y = ss_y.fit_transform(x)

        ss_z = StandardScaler()
        z = ss_z.fit_transform(z)

        timestamp_train_x, timestamp_test_x, x_train, x_test =\
         train_test_split(timestamp, x, test_size=0.1, random_state=3)
        timestamp_train_y, timestamp_test_y, y_train, y_test =\
         train_test_split(timestamp, y, test_size=0.1, random_state=3)
        timestamp_train_z, timestamp_test_z, z_train, z_test =\
         train_test_split(timestamp, x, test_size=0.1, random_state=3)

        svr_rbf = SVR(kernel='rbf', C=1e3, gamma=1, epsilon=0.0001, degree=1)
        svr_rbf_x = svr_rbf.fit(timestamp_train_x, x_train).predict(timestamp_test_x)

        print(svr_rbf)

        plt.plot(timestamp, x, 'ro', color='g', markersize=2)
        plt.plot(timestamp_test_x, svr_rbf_x, 'ro', color='r', markersize=2)
        plt.show()

    def predict(self, prn, ):
        """Predicts the position of a satellite using

        This function is called after the fit method. It will predict the
        """

sp3 = Sp3()
sp3.parse('/home/anonyme/igu18222_00.sp3')
sp3.dataset = sp3.dataset[(sp3.dataset['PRN']=='G01') & (sp3.dataset['date_time']<'2014-09-12 00:00:00')]
sp3.fit()
print(sp3.dataset.head())