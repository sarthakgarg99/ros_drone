import rospy
from sensor_msgs.msg import NavSatFix
import numpy as np
import sys
size = 64000

def talker():
    pub = rospy.Publisher('chatter_gps', NavSatFix, queue_size=10)
    rospy.init_node('talker_gps', anonymous=True)
    while not rospy.is_shutdown():
        msg = NavSatFix()
        msg.header.stamp = rospy.Time.now()
        msg.latitude = 2.34
        msg.longitude = 5.43
        msg.altitude = 5.43
        pub.publish(msg)

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
