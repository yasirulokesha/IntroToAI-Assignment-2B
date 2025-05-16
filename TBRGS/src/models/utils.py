import numpy as np
import pandas as pd
import joblib

# Custom function
def replace_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    df[column] = np.where(df[column] < lower, lower, np.where(df[column] > upper, upper, df[column]))
    return df

def generating_sequences(data_set, time_steps=24):
    x, y = [], []
    for i in range(len(data_set) - time_steps):
        x.append(data_set[i:(i + time_steps), 0])
        y.append(data_set[i + time_steps, 0])
    x = np.array(x)
    y = np.array(y)
    x = np.reshape(x, (x.shape[0], x.shape[1], 1))
    return x, y