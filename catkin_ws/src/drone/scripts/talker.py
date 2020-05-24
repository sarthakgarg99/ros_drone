#!/usr/bin/env python

import rospy
from sensor_msgs.msg import CompressedImage
import numpy as np
import sys
from Crypto.Cipher import AES
import base64
import Padding

key='qwerty'
salt='241fa86763b85341'

size = 512
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

def encrypt(plaintext,key, mode,salt):
    key,iv=get_key_and_iv(key,salt)
    
    encobj = AES.new(key,mode,iv)
    return(encobj.encrypt(plaintext.encode()))


def talker():
    pub = rospy.Publisher('cam_data', CompressedImage, queue_size=10)
    pub_enc = rospy.Publisher('cam_data_enc', CompressedImage, queue_size=10)
    rospy.init_node('drone_cam', anonymous=True)

    # rate = rospy.Rate(50) # 10hz
    # a = ""
    # for i in range(0,size):
    #     a = a + "a"
    # rospy.loginfo(sys.getsizeof(a))
    while not rospy.is_shutdown():
        msg = CompressedImage()
        msg.header.stamp = rospy.Time.now()
        msg.format = "jpeg"
        msg.data = np.zeros((10,10)).tostring()
        pub.publish(msg)
        msg_enc = CompressedImage()
        msg_enc.header.stamp = rospy.Time.now()
        msg_enc.format = "jpeg"
        msg_enc.data = encrypt(Padding.appendPadding(np.zeros((10,10)).tostring(),mode='CMS'), key, AES.MODE_CBC, salt)
        pub_enc.publish(msg_enc)
        # rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
