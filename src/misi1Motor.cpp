#include <iostream>
#include <ros/ros.h>
#include <mavros_msgs/OverrideRCIn.h>
#include <std_msgs/Float64.h>

float control_effort;
ros::Publisher motor_pub;

void controlEffort_callback(const std_msgs::Float64::ConstPtr msg){
    control_effort = msg->data;

    mavros_msgs::OverrideRCIn rcin;
    rcin.channels[3] = 1500 + control_effort;
    rcin.channels[4] = 1500 + control_effort;
    rcin.channels[5] = 1500 + control_effort;
    rcin.channels[6] = 1500 + control_effort;
    motor_pub.publish(rcin);
}

int main(int argc, char **argv){
    ros::init(argc, argv, "misi1Motor");
    ros::NodeHandle nh;

    motor_pub = nh.advertise<mavros_msgs::OverrideRCIn>("/mavros/rc/override", 8);
    ros::Subscriber controleffort_sub = nh.subscribe("control_effort/misi1", 8, controlEffort_callback);

    ros::spin();
}