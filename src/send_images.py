#!/usr/bin/python3

import rospy
from sensor_msgs.msg import Image
import cv2
import numpy as np
import socket
import struct
import pickle


HOST='192.168.1.20' 
PORT=8486
MAX_IMAGES = 60

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
connection = client_socket.makefile('wb')

def image_callback(image_data):
    #print(image_data.data)
   # print(image_data)

    
    try:
       cv_image = np.frombuffer(image_data.data, dtype=np.uint8).reshape(image_data.height, image_data.width, -1) 
    except CvBridgeError as e:
        print(e)

    else:
        #cv2.imwrite('camera_image.jpeg', cv2_img)
   # retval, buf = 
  #  number_of_bytes = len(buf)
 #   header = "" + str(number_of_bytes) + "\0"
#    raw_header = bytes(header, "utf-8")

        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

        result, frame = cv2.imencode('.jpg', cv_image, encode_param)
        data = pickle.dumps(frame, 0)
        size = len(data)
        client_socket.sendall(struct.pack(">L", size) + data)


     #   client_socket.send(raw_header)
    #    client_socket.send(buf)

        # print(f"{img_counter}: {size}")
#        client_socket.sendall(cv2_img)
    print("Sent") 

    # Send over websockets


def main():
    rospy.init_node('image_listener')
    image_topic = "/camera/rgb/image_raw"
    rospy.Subscriber(image_topic, Image, image_callback)
    rospy.spin()


if __name__ == '__main__':
    main()









