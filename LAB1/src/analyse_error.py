#!/usr/bin/env python
from dataclasses import field
import rosbag
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from mpl_toolkits import mplot3d
import bagpy
from bagpy import bagreader

#Take the bag file convert to csv and read the /gps data for stationary data.
reader_stat = bagreader('stationary_data.bag')
stat_data = reader_stat.message_by_topic('/gps')
stat_df = pd.read_csv(stat_data)

#Take the bag file convert tot csv and read the /gps data for walking data 1
reader_moving = bagreader('walking_data.bag')
moving_data = reader_moving.message_by_topic('/gps')
moving_df = pd.read_csv(moving_data)


x = 'UTM_easting'
y = 'UTM_northing'

# stat_df[x] = stat_df[x] - 328200.0000000
# stat_df[y] = stat_df[y] - 4689400.0000000

easting_data = stat_df[x].to_numpy()
northing_data = stat_df[y].to_numpy()

print("--------------------------")
print(np.cov(easting_data,northing_data, bias = True))
print(np.std(easting_data))
print(np.std(northing_data))
print(np.sqrt(np.mean(easting_data**2)))
print(np.sqrt(np.mean(northing_data**2)))




# moving_df[x] = moving_df[x] - 328200.0000000
# moving_df[y] = moving_df[y] - 4689400.0000000

easting_data = moving_df[x].to_numpy()
northing_data = moving_df[y].to_numpy()


print("--------------------------")
print(np.cov(easting_data,northing_data, bias = True))
print(np.std(easting_data))
print(np.std(northing_data))
print(np.sqrt(np.mean(easting_data**2)))
print(np.sqrt(np.mean(northing_data**2)))


b = bagreader('walking_2.bag')
data = b.message_by_topic('/gps')
df_walking = pd.read_csv(data)

easting_data = df_walking[x].to_numpy()
northing_data = df_walking[y].to_numpy()

print("--------------------------")
print(np.cov(easting_data,northing_data, bias = True))
print(np.std(easting_data))
print(np.std(northing_data))
print(np.sqrt(np.mean(easting_data**2)))
print(np.sqrt(np.mean(northing_data**2)))
