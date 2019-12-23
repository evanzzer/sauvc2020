#include <iostream>
#include <ros/ros.h>
#include <sensor_msgs/Joy.h>
#include <mavros_msgs/OverrideRCIn.h>

using namespace std;

ros::Publisher override_publisher;


void joyCallback(const sensor_msgs::Joy::ConstPtr& msg) {
    if (msg->buttons[0] == 1) {
        mavros_msgs::OverrideRCIn rcin;
        rcin.channels[0] = 1600;
        rcin.channels[1] = 1600;
        rcin.channels[2] = 1600;
        rcin.channels[3] = 1600;
        override_publisher.publish(rcin);
        ROS_INFO("Lurus");
    }  else if (msg->buttons[1] == 1) {
        mavros_msgs::OverrideRCIn rcin;
        rcin.channels[0] = 1600;
        rcin.channels[1] = 1400;
        rcin.channels[2] = 1600;
        rcin.channels[3] = 1400;
        override_publisher.publish(rcin);
        ROS_INFO("Geser Kanan");
    } else if (msg->buttons[3] == 1) {
        mavros_msgs::OverrideRCIn rcin;
        rcin.channels[0] = 1400;
        rcin.channels[1] = 1600;
        rcin.channels[2] = 1400;
        rcin.channels[3] = 1600;
        override_publisher.publish(rcin);
        ROS_INFO("Geser Kiri");
    } else if (msg->axes[0] == -1 && msg->axes[2] == -1) {
        mavros_msgs::OverrideRCIn rcin;
        rcin.channels[0] = 1600;
        rcin.channels[1] = 1400;
        rcin.channels[2] = 1400;
        rcin.channels[3] = 1600;
        override_publisher.publish(rcin);
        ROS_INFO("Putar Kanan");
    } else if (msg->axes[0] == 1 && msg->axes[2] == 1) {
        mavros_msgs::OverrideRCIn rcin;
        rcin.channels[0] = 1400;
        rcin.channels[1] = 1600;
        rcin.channels[2] = 1600;
        rcin.channels[3] = 1400;
        override_publisher.publish(rcin);
        ROS_INFO("Putar Kiri");
    } else if (msg->buttons[1] == -1) {
        mavros_msgs::OverrideRCIn rcin;
        rcin.channels[4] = 1600;
        rcin.channels[5] = 1600;
        override_publisher.publish(rcin);
        ROS_INFO("Tenggelam");
    }else if (msg->buttons[1] == 1) {
        mavros_msgs::OverrideRCIn rcin;
        rcin.channels[4] = 1400;
        rcin.channels[5] = 1400;
        override_publisher.publish(rcin);
        ROS_INFO("Angkat");
    }
    else{
        mavros_msgs::OverrideRCIn rcin;
        rcin.channels[0] = 1500;
        rcin.channels[1] = 1500;
        rcin.channels[2] = 1500;
        rcin.channels[3] = 1500;
        override_publisher.publish(rcin);
        ROS_INFO("Diem");
    }
}


int main(int argc, char **argv) {
    ros::init(argc, argv, "testservo");
    ros::NodeHandle nh;

    override_publisher = nh.advertise<mavros_msgs::OverrideRCIn>("/mavros/rc/override", 8);

    ros::Subscriber joy_subscriber = nh.subscribe("joy", 8, joyCallback);
    ros::spin();

}
