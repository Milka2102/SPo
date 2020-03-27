#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import SetPen
from turtlesim.srv import TeleportAbsolute
import std_srvs.srv
import math
import time

horizontal = [
    [1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0],
    [1, 0, 1, 1, 1, 0]
]

vertical = [
    [0, 1],
    [1, 0],

    [1, 0],
    [1, 1],

    [0, 0],
    [1, 1],

    [1, 0],
    [1, 1],

    [0, 1],
    [0, 1],

    [0, 0],
    [1, 1],
]



class TurtleBot:

    def __init__(self):
        rospy.init_node('robot_cleaner', anonymous=True)
        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, self.when_update_pose)
        self.pose = Pose()
        self.rate = rospy.Rate(10)


    def when_update_pose(self, data):
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4) 

    def set_pen(self, isOn):
        serv1=rospy.ServiceProxy('/turtle1/set_pen',SetPen)
        color = 255 if isOn else 0
        serv1(color,color,color,5,0);


    def horizontal_move(self, start_y, array):
        self.set_pen(False)
        serv1=rospy.ServiceProxy('turtle1/teleport_absolute',TeleportAbsolute)
        serv1(0.5,start_y,0);
        time.sleep(1)
        for i in array:
            self.set_pen(False)
            if (i == 1):
                self.set_pen(True)
            vel_msg = Twist()
            vel_msg.linear.x = 1
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = 0
            self.velocity_publisher.publish(vel_msg)
            time.sleep(1)
            self.set_pen(False)
            vel_msg = Twist()
            vel_msg.linear.x = 0.5
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = 0
            self.velocity_publisher.publish(vel_msg)
            time.sleep(1)
    
    def vertical_move(self, start_x, array):
        self.set_pen(False)
        serv1=rospy.ServiceProxy('turtle1/teleport_absolute',TeleportAbsolute)
        serv1(start_x, 6, -0.5*math.pi);
        time.sleep(1)
        for i in array:
            self.set_pen(False)
            if (i == 1):
                self.set_pen(True)
            vel_msg = Twist()
            vel_msg.linear.x = 1
            self.velocity_publisher.publish(vel_msg)
            time.sleep(1)
        

    def painting(self):
        rospy.set_param("background_r",0)
        rospy.set_param("background_g",0)
        rospy.set_param("background_b",0)
        serv1=rospy.ServiceProxy('/clear',std_srvs.srv.Empty)
        serv1();
        dif_x = 0   
        for line in range(len(vertical)):
            dif_x += 0.5 if line % 2 == 0 else 1
            self.vertical_move(dif_x, vertical[line])
        for line in range(len(horizontal)):
           self.horizontal_move(6-line, horizontal[line])
        
        

if __name__ == '__main__':
  try:
    turtle = TurtleBot()
    turtle.painting()
  except rospy.ROSInterruptException:
    pass
