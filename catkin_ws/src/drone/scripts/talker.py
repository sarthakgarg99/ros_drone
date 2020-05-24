

import rospy
from sensor_msgs.msg import CompressedImage
import numpy as np
import sys
size = 64000




def talker():
    pub = rospy.Publisher('chatter', CompressedImage, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(50) # 10hz
    a = ""
    for i in range(0,size):
        a = a + "a"
    rospy.loginfo(sys.getsizeof(a))
    while not rospy.is_shutdown():
        msg = CompressedImage()
        msg.header.stamp = rospy.Time.now()
        msg.format = "jpeg"
        msg.data = np.zeros((10,10)).tostring()
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
