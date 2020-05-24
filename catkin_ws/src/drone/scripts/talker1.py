import rospy
from std_msgs.msg import String
from Crypto.Cipher import AES
import sys

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
    pub = rospy.Publisher('chatter1', String, queue_size=10)
    rospy.init_node('talker_new', anonymous=True)
    rate = rospy.Rate(50) # 10hz
    a = ""
    for i in range(0,size):
        a = a + "a"
    rospy.loginfo(sys.getsizeof(a))
    while not rospy.is_shutdown():
        a = ""
        for i in range(0,size):
            a = a + "a"
        time = rospy.get_time()
        hello_str = str(encrypt(Padding.appendPadding(a,mode='CMS'), key, AES.MODE_CBC, salt)) + "|" + str(time)
        rospy.loginfo(hello_str)
        with open("test.png", "rb")as img_file:
            mystring = base64.b64encode(img_file.read())
        rospy.loginfo(mystring)
        pub.publish(mystring)


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
