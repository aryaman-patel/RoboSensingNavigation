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

# Creating the common data to be analysed
x = "UTM_easting"
y = "UTM_northing"
z = "header.stamp.sec"

# 2D Plot of the stationary data. 
stat_df['UTM_easting'] = stat_df['UTM_easting'] - 328200.0000000
stat_df['UTM_northing'] = stat_df['UTM_northing'] - 4689400.0000000
plt.plot(stat_df.loc[:, x], stat_df.loc[:, y],'green', linewidth= 2.5)
plt.xlabel("UTM Easting 3282e+2 (m)")
plt.ylabel("UTM Northing 46894e+2 (m)")
plt.show()

# 2D Plot of the moving data. 
moving_df['UTM_easting'] = moving_df['UTM_easting'] - 328200.0000000
moving_df['UTM_northing'] = moving_df['UTM_northing'] - 4689400.0000000
plt.plot(moving_df.loc[:, x], moving_df.loc[:, y],'blue', linewidth= 2.5)
plt.xlabel("UTM Easting 3282e+2 (m)")
plt.ylabel("UTM Northing 46894e+2 (m)")
plt.show()

# 3D Plot for Stat data.
time = stat_df['header.stamp.secs'].tolist()
time[0] = 0
for x in range(1,len(time)):
    if x == len(time)-1 :
        time[x] = time[x-1] + 1
    else :
        time[x] = time[x+1] - time[x] + time[x-1]

div = time[1]
for x in range(1,len(time)):
    time[x] = time[x]/div

stat_df['header.stamp.secs'] = time
xline = stat_df['UTM_easting'].to_numpy()
yline = stat_df['UTM_northing'].to_numpy()
zline = stat_df['header.stamp.secs'].to_numpy()
ax = plt.axes(projection='3d')
ax.plot3D(xline, yline, zline, 'green', linewidth = 1.5)
ax.scatter3D(xline, yline, zline, c=zline, cmap='rainbow')
plt.xlabel("UTM Easting 3282e+2 (m)")
plt.ylabel("UTM Northing 46894e+2 (m)")
ax.set_zlabel('Time (sec)');
plt.show()


# 3D plot for walking data
time = moving_df['header.stamp.secs'].tolist()
time[0] = 0
for x in range(1,len(time)):
    if x == len(time)-1 :
        time[x] = time[x-1] + 1
    else :
        time[x] = time[x+1] - time[x] + time[x-1]
div = time[1]
for x in range(1,len(time)):
    time[x] = time[x]/div
moving_df['header.stamp.secs'] = time
xline = moving_df['UTM_easting'].to_numpy()
yline = moving_df['UTM_northing'].to_numpy()
zline = moving_df['header.stamp.secs'].to_numpy()

ax = plt.axes(projection='3d')
ax.plot3D(xline, yline, zline, 'red', linewidth = 1.5)
ax.scatter3D(xline, yline, zline, c=zline, cmap='rainbow')
plt.xlabel("UTM Easting 3282e+2 (m)")
plt.ylabel("UTM Northing 46894e+2 (m)")
ax.set_zlabel('Time (sec)');
plt.show()




# Analysis of a second walking data
b = bagreader('walking_2.bag')
data = b.message_by_topic('/gps')
df_walking = pd.read_csv(data)

df_walking['UTM_easting'] = df_walking['UTM_easting'] - 328200.0000
df_walking['UTM_northing'] = df_walking['UTM_northing'] - 4689400.0000
x = 'UTM_easting'
y = 'UTM_northing'

plt.plot(df_walking.loc[:, x], df_walking.loc[:, y],'yellow', linewidth= 2.5)
plt.xlabel('UTM Easting 3282e+2 (m)')
plt.ylabel('UTM_Northing 46894e+2 ()')
plt.show()




