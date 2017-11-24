#include "ros/ros.h"
#include "std_msgs/Float64.h"
#include "msgs_pkg/State_vector.h"
#include <stdio.h>
#include <stdlib.h>
#include <time.h>


float alt_data = 0;

void chatterCallback(const msgs_pkg::State_vector::ConstPtr& msg)
{
    ROS_INFO("Altitude received: [%f]", msg->state.linear.z);
    alt_data = msg->state.linear.z;
}



int main(int argc, char **argv)
{
    ros::init(argc, argv, "pressure_meter_publisher");
    ros::init(argc, argv, "pressure_meter_listener");
    ros::NodeHandle n;

    ros::Publisher chatter_pub = n.advertise<std_msgs::Float64>("pressure_meter_chatter", 1000);
    ros::Subscriber sub = n.subscribe("state_vector", 1000, chatterCallback);

    ros::Rate loop_rate(10);

    while (ros::ok())
      {
        /**
         * Publish depth estimation using the real position and adding a noise (very simple).
         */
        std_msgs::Float64 alt_msg;

        srand((unsigned int)time(NULL));

        float a = 0.3;
        
        alt_msg.data = alt_data - a/2 + ((float)rand()/(float)(RAND_MAX)) * a;

        ROS_INFO("Depth sent (pressure sensor): %f", alt_msg.data);

        chatter_pub.publish(alt_msg);


        ros::spinOnce();

        loop_rate.sleep();
      }


    return 0;
}
