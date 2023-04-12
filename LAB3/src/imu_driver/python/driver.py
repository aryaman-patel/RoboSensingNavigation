#!/usr/bin/env python

import sys
import rospy
from sensor_msgs.msg import Imu
from sensor_msgs.msg import MagneticField
from imu_driver.msg import imu_msg
import serial
import math
import re


class AccelParser():

    def __init__(self):

        self.sensor_data = []
        self.imu_data = imu_msg()
        self.yaw = 0.00
        self.roll = 0.00
        self.pitch = 0.00

    def conv_to_quatern(self):        
        cos_y = math.cos(math.radians(self.yaw)*0.5)
        cos_p = math.cos(math.radians(self.pitch)*0.5)
        cos_r = math.cos(math.radians(self.roll)*0.5)

        sin_y = math.sin(math.radians(self.yaw)*0.5)
        sin_p = math.sin(math.radians(self.pitch)*0.5)
        sin_r = math.sin(math.radians(self.roll)*0.5)

        self.imu_data.IMU.orientation.w = cos_r * cos_p * cos_y + sin_r * sin_p * sin_y
        self.imu_data.IMU.orientation.x = sin_r * cos_p * cos_y - cos_r * sin_p * sin_y
        self.imu_data.IMU.orientation.y = cos_r * sin_p * cos_y + sin_r * cos_p * sin_y
        self.imu_data.IMU.orientation.z = cos_r * cos_p * sin_y - sin_r * sin_p * cos_y
    
    def linear_accn(self):
        self.imu_data.IMU.linear_acceleration.x = float(self.sensor_data[7])
        self.imu_data.IMU.linear_acceleration.y = float(self.sensor_data[8])
        self.imu_data.IMU.linear_acceleration.z = float(self.sensor_data[9])

    def ang_accn(self):
        self.imu_data.IMU.angular_velocity.x = float(self.sensor_data[10])
        self.imu_data.IMU.angular_velocity.y = float(self.sensor_data[11])
        velo_z = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", self.sensor_data[12])
        self.imu_data.IMU.angular_velocity.z = float(velo_z[0])

    def mag_data(self):
        self.imu_data.MagField.magnetic_field.x = float(self.sensor_data[4])
        self.imu_data.MagField.magnetic_field.y = float(self.sensor_data[5])
        self.imu_data.MagField.magnetic_field.z = float(self.sensor_data[6])


    def parser(self, data):
        
        if data.startswith("$VNYMR"):
            self.sensor_data = data.split(",")
            self.imu_data.Header.frame_id = "IMU1_Frame"
            self.imu_data.Header.stamp = rospy.Time.now()
            self.yaw = float(self.sensor_data[1])
            self.pitch = float(self.sensor_data[2])
            self.roll = float(self.sensor_data[3])
            self.conv_to_quatern()
            self.linear_accn()
            self.ang_accn()
            self.mag_data()
            #rospy.loginfo(self.sensor_data)


   

if __name__ == '__main__':

    args = rospy.myargv(argv = sys.argv)
    if len(args) != 2:
        print("Error in input parameters!")
        print("Example Command: rosrun imu_driver driver.py /dev/ttyUSB0")

    rospy.init_node('IMU_node')
    PORT = args[1]
    BAUD = 115200
    port = serial.Serial(PORT, BAUD, timeout=2.0)
    rospy.loginfo(port)
    pub = rospy.Publisher('imu', imu_msg, queue_size = 5)
    rospy.sleep(0.2)
    port.write(str.encode("$VNWRG,07,40*59"))
    port.write(str.encode("$VNWRG,06,14*6C"))
    sensor_driver = AccelParser()

    try:
        while not rospy.is_shutdown():
            DATA = str(port.readline())[2:]
            #rospy.loginfo(DATA)
            sensor_driver.parser(DATA)
            pub.publish(sensor_driver.imu_data)



    except rospy.ROSInterruptException:
        port.close()
    except serial.serialutil.SerialException:
        rospy.lofinfo("Shutting down gps node ...")
