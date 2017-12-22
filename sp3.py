#!/usr/bin/env python
import numpy as np
import pandas as pd

def read_sp3(file_path):
    df = pd.DataFrame()
    with open(file_path) as fp:
        for line in fp:
            if '*  ' in line:
                date_time = line.split()[1:len(line.split())]
                line = fp.next()
                while '*  ' not in line:
                    line = fp.next()
                    data_table = data_table.append(date_time+line.split())
    print(data_table)           

read_sp3('/home/anonyme/igu18222_00.sp3')
