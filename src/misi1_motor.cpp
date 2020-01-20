#include <iostream>
#include <ros/ros.h>
#include <mavros_msgs/OverrideRCIn.h>
#include <std_msgs/Float64.h>

using namespace std;

float control_effort;
int i=0, toleransi = 20;
ros::Publisher motor_pub;

void control_effort_callback(const std_msgs::Float64::ConstPtr msg){
    control_effort = msg->data;
    mavros_msgs::OverrideRCIn rcin;
    if(abs(control_effort) == toleransi){
        // maju
        rcin.channels[1] = 1650;
        rcin.channels[2] = 1650;
        rcin.channels[3] = 1650;
        rcin.channels[4] = 1650;
        motor_pub.publish(rcin);
        cout << control_effort << endl;
    }
    else{
        // belok-belok
        rcin.channels[1] = 1500 - control_effort ;
        rcin.channels[2] = 1500 + control_effort;
        rcin.channels[3] = 1500 + control_effort;
        rcin.channels[4] = 1500 - control_effort;
        motor_pub.publish(rcin);
        cout << control_effort << endl;
    }
}

void start(){
    mavros_msgs::OverrideRCIn rcin;
    for(i=0; i<8; i++){
        rcin.channels[i] = 1500;
    }
    motor_pub.publish(rcin);
    cout << "start" << endl;
}

int main(int argc, char **argv){
    ros::init(argc, argv, "kualifikasi_PID_controleffort");
    ros::NodeHandle nh;
    cout << "test" << control_effort << endl;
    motor_pub = nh.advertise<mavros_msgs::OverrideRCIn>("/mavros/rc/override", 8);

    ros::Subscriber controleffort_sub = nh.subscribe("misi1/control_effort", 8, control_effort_callback);
    start();
    ros::spin();
}