"""
This script plots the calibration data that is used for
checking if all sensors are calibrated to the same temperature
"""

# coding: utf-8
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

df = pd.read_csv('calibrages.csv')

# simple scatter plot to visualise correlation
plt.scatter(df.temperature1, df.temperature2)
plt.plot([13, 19], [13, 19], linestyle=':')
plt.xlabel('Temperature of sensor 1')
plt.ylabel('Temperature of sensor 2')
plt.show()

# histogram of absolute differences
df['abserror'] = np.abs(df['temperature1'] - df['temperature2'])
df['abserror'].hist()
plt.xlabel('absolute error in degrees Celsius')
plt.ylabel('number of readings')
plt.title('Difference between two sensors')
plt.show()

# boxplot of differences for each pair of sensors
df['error'] = df['temperature1'] - df['temperature2']
    
def add_sorted_pair_label(row):
    sensors = sorted([row['sensor1'], row['sensor2']])
    return '-'.join(sensors)
    
#df['pair'] = df.apply(add_sorted_pair_label, axis=1)
df['pair'] = df.apply(lambda row: '-'.join(sorted([row['sensor1'],
                                                   row['sensor2']])),
                      axis=1)
sns.boxplot(data=df, x='pair', y='error')
plt.plot([0, df['pair'].nunique()], [0, 0], linestyle=':')
plt.xlabel('pair of sensors')
plt.ylabel('temperature difference / degrees')
plt.show()

# heatmap of temperature difference matrix
df_inv = pd.DataFrame({"sensor1": df["sensor2"].values,
                       "sensor2": df["sensor1"].values,
                       "temperature1": df["temperature2"].values,
                       "temperature2": df["temperature1"].values})
df_all = pd.concat((df, df_inv))

df_all['error'] = df_all['temperature1'] - df_all['temperature2']
df_g = df_all.groupby(['sensor1',
                       'sensor2'], as_index=False)['error'].median()
df_p = df_g.pivot(index="sensor1", columns="sensor2", values="error")
sns.heatmap(df_p, cmap='coolwarm', vmin=-0.4, vmax=+0.4)
plt.title('Median delta-temperature value for each sensor pair')
plt.show()
