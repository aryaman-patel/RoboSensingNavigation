#!/usr/bin/env python      
import rospy
from std_msgs.msg import String


#Initializing the node. 
rospy.init_node('Talker')
chatter = 'She sells sea shells on the sea shore.'
#Setting up the publisher.
publisher = rospy.Publisher('the_tele_line',String,queue_size = 5)   #The message yet to be announced

rate = rospy.Rate(1)                        # Rate of publishing the message

while not rospy.is_shutdown():
	publisher.publish(chatter)              #Message here
	rospy.loginfo(chatter)
	rate.sleep()

