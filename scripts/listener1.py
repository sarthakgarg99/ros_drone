

import rospy
from std_msgs.msg import String
from Crypto.Cipher import AES
import sys

import base64
import Padding
num = 0
sum = 0
key='qwerty'
salt='241fa86763b85341'
time_pub = 0;
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
    a = data.data.rsplit("|",1)[0];
    m = decrypt(a,key,AES.MODE_CBC,salt)
    global num
    global time_pub;
    if(num == 0):
        time_pub = float(data.data.split('|')[-1]);
    # rospy.loginfo(int(time_rec * 10000) - time_pub);

    global sum
    num += 1;
    if(num % 1000 == 0):
        rospy.loginfo(str(num) + ": " + str(rospy.get_time() - time_pub))

    # rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener_new', anonymous=True)

    rospy.Subscriber('chatter1', String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
