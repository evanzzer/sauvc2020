#include <iostream>
#include <ros/ros.h>
#include <mavros_msgs/OverrideRCIn.h>
#include <std_msgs/Float64.h>
#include <chrono>

float control_effort;
int i=0;
ros::Publisher motor_pub;

void controlEffort_callback(const std_msgs::Float64::ConstPtr msg){
    control_effort = msg->data;

    mavros_msgs::OverrideRCIn rcin;
    rcin.channels[5] = 1500 + control_effort;
    rcin.channels[6] = 1500 + control_effort;
    motor_pub.publish(rcin);
}

void start(){
    mavros_msgs::OverrideRCIn rcin;
    for(i=0; i<8; i++){
        rcin.channels[i] = 1500;
    }
    motor_pub.publish(rcin);
    sleep(2);
    rcin.channels[5] = 1600;
    rcin.channels[6] = 1600;
    motor_pub.publish(rcin);
    sleep(1);
    rcin.channels[1] = 1600;
    rcin.channels[2] = 1600;
    rcin.channels[3] = 1600;
    rcin.channels[4] = 1600;
    rcin.channels[5] = 1500;
    rcin.channels[6] = 1500;
    motor_pub.publish(rcin);
}

int main(int argc, char **argv){
    ros::init(argc, argv, "kualifikasi_PID_controleffort");
    ros::NodeHandle nh;

    motor_pub = nh.advertise<mavros_msgs::OverrideRCIn>("/mavros/rc/override", 8);

    ros::Subscriber controleffort_sub = nh.subscribe("kualifikasi/control_effort", 8, controlEffort_callback);
    start();
    ros::spin();
}