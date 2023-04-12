#! /usr/bin/env python
import rospy
import sys
from PA1.srv import*




if len(sys.argv) == 3:
	inp_1 = float(sys.argv[1])
	inp_2 = float(sys.argv[2])

else:
	print("Please input 2 floats!!")
	sys.exit(1)



rospy.wait_for_service('multiply_floats')
multiply_floats = rospy.ServiceProxy('multiply_floats',the_multiplier)

result = multiply_floats(inp_1,inp_2)
print("The result is : ", result.ans)
