#!/usr/bin/env python

import time
from datetime import date
import rospy
import serial
import utm.conversion as utm
from gps_driver.msg import gps_msg
import sys



class GPS_PARSER():

	def __init__(self):
		self.pattern = '%d%m%Y%H%M%S.%f'
		self.lat_data = 0
		self.long_data = 0
		self.today = date.today().strftime("%d%m%Y")
		self.pub = rospy.Publisher('gps', gps_msg, queue_size = 5)
		self.gps_data = gps_msg()
		self.data = []

	def convert_to_epoch(self):
		date_time = self.today + self.data[1]
		print(date_time)
		self.gps_data.Header.stamp.secs =  int(time.mktime(time.strptime(date_time, self.pattern)))

	def convert_to_utm(self):
		utm_data = utm.from_latlon(self.lat_data, self.long_data)
		self.gps_data.UTM_easting = utm_data[0]
		self.gps_data.UTM_northing = utm_data[1]
		self.gps_data.Zone = utm_data[2]
		self.gps_data.Letter = utm_data[3]
		#print(utm_data)
		
		
	def define_lat_long_alt(self):		
		lat = self.data[2]
		lon = self.data[4]
		self.gps_data.Altitude = float(self.data[9])

		dir1 = lambda x : 1 if (x == 'N') else -1
		dir2 = lambda x : 1 if (x == 'E') else -1
		
		self.lat_data = dir1(self.data[3])*(float(lat[:2])+float(lat[2:])/60)		
		self.long_data = dir2(self.data[5])*(float(lon[:3]) + float(lon[3:])/60)		
		self.gps_data.Latitude = self.lat_data
		self.gps_data.Longitude = self.long_data
		self.gps_data.Header.frame_id = "GPS1_Frame"
		


	def parser(self, line):
		if line.startswith("$GPGGA"):
			self.data = line.split(",")
			rospy.loginfo(self.data)

			

			if self.data[2] == '':
				rospy.logwarn("Unable to collect location data, please reposition yourself!!")
			else:				
				self.convert_to_epoch()
				self.define_lat_long_alt()
				self.convert_to_utm()
				self.pub.publish(self.gps_data)




if __name__ == '__main__':
	
	args = rospy.myargv(argv=sys.argv)
	if len(args) != 2:
		print("Error in input parameters!")
		print("Please make sure the command is of the format: roslaunch gps_driver driver.launch /dev/ttyACM0")
		
	rospy.init_node('sensor_node')
	#serial_port = rospy.get_param('/rosbag_record_gps_data/port')  #Should be user defined.
	serial_baud = rospy.get_param('~baudrate',4800)
	rospy.logdebug("GPS sensor recognised on port " + args[1] + " at " + str(serial_baud))
	port = serial.Serial(args[1], serial_baud, timeout = 1.0)
	rospy.logdebug("GPS sensor recognised on port " + args[1] + " at " + str(serial_baud))
	rospy.logdebug("Initializing sensor ...")
	pub = rospy.Publisher('gps', gps_msg, queue_size = 5)
	rospy.sleep(0.2)
	rospy.Rate(10)


	sensor_driver = GPS_PARSER()

	try:
		while not rospy.is_shutdown():
			line = str(port.readline())[4:]
			rospy.loginfo(line)
			sensor_driver.parser(line)	
			rospy.sleep(0.01)

	except rospy.ROSInterruptException:
		port.close()
	except serial.serialutil.SerialException:
		rospy.lofinfo("Shutting down gps node ...")

