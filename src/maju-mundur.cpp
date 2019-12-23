#include <iostream>
#include <ros/ros.h>
#include <mavros_msgs/OverrideRCIn.h>
#include <chrono>

ros::Publisher motor_pub;

void naik(std::chrono::milliseconds ms){
    std::chrono::time_point<std::chrono::system_clock> end;
    end = std::chrono::system_clock::now() + ms;
    while(std::chrono::system_clock::now() < end){
        mavros_msgs::OverrideRCIn rcin;
        rcin.channels[1] = 1600;
        rcin.channels[2] = 1600;
        motor_pub.publish(rcin);
    }
}

void turun(std::chrono::milliseconds ms){
    std::chrono::time_point<std::chrono::system_clock> end;
    end = std::chrono::system_clock::now() + ms;
    while(std::chrono::system_clock::now() < end){
        mavros_msgs::OverrideRCIn rcin;
        rcin.channels[1] = 1400;
        rcin.channels[2] = 1400;
        motor_pub.publish(rcin);
    }
}

void maju(std::chrono::milliseconds ms){
    std::chrono::time_point<std::chrono::system_clock> end;
    end = std::chrono::system_clock::now() + ms;
    while(std::chrono::system_clock::now() < end){
        mavros_msgs::OverrideRCIn rcin;
        rcin.channels[3] = 1600;
        rcin.channels[4] = 1600;
        rcin.channels[5] = 1600;
        rcin.channels[6] = 1600;
        motor_pub.publish(rcin);
    }
}

void mundur(std::chrono::milliseconds ms){
    std::chrono::time_point<std::chrono::system_clock> end;
    end = std::chrono::system_clock::now() + ms;
    while(std::chrono::system_clock::now() < end){
        mavros_msgs::OverrideRCIn rcin;
        rcin.channels[3] = 1400;
        rcin.channels[4] = 1400;
        rcin.channels[5] = 1400;
        rcin.channels[6] = 1400;
        motor_pub.publish(rcin);
    }
}

int main(int argc, char **argv){
    ros::init(argc, argv, "maju-mundur");
    ros::NodeHandle nh;

    motor_pub = nh.advertise<mavros_msgs::OverrideRCIn>("/mavros/rc/override", 8);

    std::chrono::milliseconds ms(1000);
    while(1){
        turun(ms);
        delay(1000);
        naik(ms);
        delay(1000);
        maju(ms);
        delay(1000);
        mundur(ms);
        delay(1000);
    }  
}