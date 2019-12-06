#include <iostream>
#include <ros/ros.h>
#include <mavros_msgs/OverrideRCIn.h>
#include <std_msgs/Float64.h>
#include <chrono>

float control_effort;
ros::Publisher motor_pub;

void controlEffort_callback(const std_msgs::Float64::ConstPtr msg){
    control_effort = msg->data;

    mavros_msgs::OverrideRCIn rcin;
    rcin.channels[0] = 1500 + control_effort;
    rcin.channels[1] = 1500 + control_effort;
    motor_pub.publish(rcin);
}

void run(std::chrono::milliseconds ms){
    std::chrono::time_point<std::chrono::system_clock> end;
    end = std::chrono::system_clock::now() + ms;
    while(std::chrono::system_clock::now() < end){
        ros::spin();
    }
}

int main(int argc, char **argv){
    ros::init(argc, argv, "kualifikasi_PID_controleffort");
    ros::NodeHandle nh;

    motor_pub = nh.advertise<mavros_msgs::OverrideRCIn>("/mavros/rc/override", 8);
    ros::Subscriber controleffort_sub = nh.subscribe("control_effort", 8, controlEffort_callback);
    
    std::chrono::milliseconds ms(5000);
    run(ms);  
}