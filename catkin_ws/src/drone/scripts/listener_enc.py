#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import CompressedImage
from Crypto.Cipher import AES
import numpy as np


import base64
import Padding
key='qwerty'
salt='241fa86763b85341'

def get_key_and_iv(password, salt, klen=32, ilen=16, msgdgst='md5'):

    mdf = getattr(__import__('hashlib', fromlist=[msgdgst]), msgdgst)
    password = password.encode('ascii', 'ignore')  # convert to ASCII
    salt = bytearray.fromhex(salt) # convert to ASCII

    try:
        maxlen = klen + ilen
        keyiv = mdf((password + salt)).digest()
        tmp = [keyiv]
        while len(tmp) < maxlen:
            tmp.append( mdf(tmp[-1] + password + salt).digest() )
            keyiv += tmp[-1]  # append the last byte
        key = keyiv[:klen]
        iv = keyiv[klen:klen+ilen]
        return key, iv
    except UnicodeDecodeError:
         return None, None

def decrypt(ciphertext,key, mode,salt):
    key,iv=get_key_and_iv(key,salt)
    encobj = AES.new(key,mode,iv)
    return(encobj.decrypt(ciphertext))


def callback(data):
    a = decrypt(data.data,key,AES.MODE_CBC,salt)
    # time.sleep(1);
    np_arr = np.fromstring(a, np.uint8)
    rospy.loginfo(np_arr)
    t1 = rospy.Time.now()
    t2 = data.header.stamp

    rospy.loginfo(str(t1) + " " + str(t2) + " " + str(t1 - t2))

    # rospy.loginfo(int(time_rec * 10000))
    # rospy.loginfo(int(time_pub*10000))



def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener_enc', anonymous=True)

    rospy.Subscriber('cam_data_enc', CompressedImage, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
