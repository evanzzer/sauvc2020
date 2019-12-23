#include <iostream>
#include <ros/ros.h>
#include <mavros_msgs/OverrideRCIn.h>
#include <chrono>
#include <std_msgs/Int16.h>

using namespace std;

ros::Publisher motor_pub;
int oke;

void naik(){
        mavros_msgs::OverrideRCIn rcin;
        for (int i = 0; i < 8; i++) rcin.channels[i] = 1500;
        rcin.channels[5] = 1600;
        rcin.channels[6] = 1600;
	cout << "naik" << endl;
        motor_pub.publish(rcin);
}

void turun(){
        mavros_msgs::OverrideRCIn rcin;
        for (int i = 0; i < 8; i++) rcin.channels[i] = 1500;
        rcin.channels[5] = 1400;
        rcin.channels[6] = 1400;
	cout << "turun" << endl;
        motor_pub.publish(rcin);
}

void maju(){
        mavros_msgs::OverrideRCIn rcin;
        for (int i = 0; i < 8; i++) rcin.channels[i] = 1500;
        rcin.channels[1] = 1550;
        rcin.channels[2] = 1550;
        rcin.channels[3] = 1550;
        rcin.channels[4] = 1550;
	cout << "maju" << endl;
        motor_pub.publish(rcin);
}

void all(){
        mavros_msgs::OverrideRCIn rcin;
	rcin.channels[7] = 1600;
        // for (int i = 0; i < 8; i++) rcin.channels[i] = 1600;
	// cout << "maju" << endl;
        motor_pub.publish(rcin);
}


void mundur(){
	mavros_msgs::OverrideRCIn rcin;
        for (int i = 0; i < 8; i++) rcin.channels[i] = 1500;
        rcin.channels[1] = 1450;
        rcin.channels[2] = 1450;
        rcin.channels[3] = 1450;
        rcin.channels[4] = 1450;
	cout << "mundur" << endl;
        motor_pub.publish(rcin);
}

void release(){
        mavros_msgs::OverrideRCIn rcin;
	rcin.channels[0] = 0;
	rcin.channels[1] = 0;
	rcin.channels[2] = 0;
        rcin.channels[3] = 0;
        rcin.channels[4] = 0;
        rcin.channels[5] = 0;
        rcin.channels[6] = 0;
	rcin.channels[7] = 0;
	cout << "start" << endl;
        motor_pub.publish(rcin);	
}


void start(){
        mavros_msgs::OverrideRCIn rcin;
	for (int i = 0; i < 8; i++) rcin.channels[i] = 1500;
	cout << "start" << endl;
        motor_pub.publish(rcin);	
}


void killcallback(const std_msgs::Int16::ConstPtr msg){
	oke = msg->data;
	if(oke==1){
		cout << "mati" << endl;
	        start();
		sleep(2);	
	}
	else{
		cout << "hidup" << endl;
		naik();
		sleep(2);
		turun();
		sleep(2);
	}
}

int main(int argc, char **argv){
    ros::init(argc, argv, "majumundur");
    ros::NodeHandle nh;

    motor_pub = nh.advertise<mavros_msgs::OverrideRCIn>("/mavros/rc/override", 8);

    ros::Subscriber killswitch_sub = nh.subscribe("kill_switch", 8, killcallback);

    release();
    sleep(2);
    start();
    sleep(5);
ros::spin();
/*    while(ros::ok() && oke == 0){	
ros::spinOnce();	
maju();
	sleep(2);
	mundur();
	sleep(2);
	
}*/



}
