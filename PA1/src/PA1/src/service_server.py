#! /usr/bin/env python
import rospy
from PA1.srv import the_multiplier, the_multiplierResponse

def service_handler_function(inp):
	print("Returning [%f * %f = %f]"%(inp.a, inp.b, (inp.a*inp.b)))
	return the_multiplierResponse(inp.a*inp.b)


rospy.init_node('float_multiplier_server')

s = rospy.Service('multiply_floats',the_multiplier, service_handler_function)


rospy.spin()
