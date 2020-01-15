#include <std_msgs/Int16.h>
#include <iostream>
#include <ros/ros.h>
#include <mavros_msgs/OverrideRCIn.h>

using namespace std;

ros::Publisher motor_pub;
int oke;

void killcallback(const std_msgs::Int16::ConstPtr msg){
	oke = msg->data;
	if(oke==1){
        	mavros_msgs::OverrideRCIn rcin;
		rcin.channels[1] = 0;
		rcin.channels[2] = 0;
		rcin.channels[3] = 0;
        	rcin.channels[4] = 0;
        	rcin.channels[5] = 0;
       		rcin.channels[6] = 0;
        	motor_pub.publish(rcin);
	}
}

int main(int argc, char **argv){
    ros::init(argc, argv, "kualifikasi_PID_controleffort");
    ros::NodeHandle nh;

    motor_pub = nh.advertise<mavros_msgs::OverrideRCIn>("/mavros/rc/override", 8);
    ros::Subscriber controleffort_sub = nh.subscribe("kill_switch", 8, killcallback);

	ros::spin();
}
