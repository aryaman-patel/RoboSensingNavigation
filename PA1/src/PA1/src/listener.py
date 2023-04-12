#!/usr/bin/env python
import rospy
from std_msgs.msg import String


rospy.init_node('Listener')


def callback(msg):
	msg = str(msg)[5:]
	chatter = msg[30:-2].join(part.replace('sea shore','sea shells') for part in msg.split('sea shells'))
	rospy.loginfo('I heard: %s', chatter)

subscriber = rospy.Subscriber('the_tele_line', String, callback)

rospy.spin()