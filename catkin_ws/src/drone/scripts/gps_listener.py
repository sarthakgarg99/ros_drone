import rospy
from sensor_msgs.msg import NavSatFix
import numpy as np

def callback(data):
    a = data
    lat = a.latitude
    lon = a.longitude
    alt = a.altitude
    rospy.loginfo(a)
    rospy.loginfo(str(lat) + " " + str(lon) + " " + str(alt))

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber('chatter_gps', NavSatFix, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
