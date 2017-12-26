#!/usr/bin/env python
import numpy as np
import pandas as pd


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

    def fit(self):
        """fit the model"""

    def predict(self, prn, ):
        """Predicts the position of a satellite using

        This function is called after the fit method. It will predict the
        """


sp3 = Sp3()
sp3.parse('/home/anonyme/igu18222_00.sp3')
