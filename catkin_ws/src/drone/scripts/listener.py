#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import CompressedImage
import numpy as np
num = 0
sum = 0
def callback(data):
    a = data.data;
    # time.sleep(1);
    np_arr = np.fromstring(data.data, np.uint8)
    rospy.loginfo(np_arr)

    # rospy.loginfo(int(time_rec * 10000))
    # rospy.loginfo(int(time_pub*10000))


def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber('chatter', CompressedImage, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
