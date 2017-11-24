#include "ros/ros.h"
#include "std_msgs/Float64.h"
#include "msgs_pkg/State_vector.h"


// Publish the state vector estimation in the "state_vector" topic.

int main(int argc, char **argv)
{
    ros::init(argc, argv, "state_vector_publisher");
    ros::NodeHandle n;

    ros::Publisher state_pub = n.advertise<msgs_pkg::State_vector>("state_vector", 1000);

    ros::Rate loop_rate(10);

    while (ros::ok())
      {
        /**
         * Publish state vector estimation.
         */
        msgs_pkg::State_vector state_msg;


        // Values
        state_msg.state.linear.x = 1;
        state_msg.state.linear.y = 1;
        state_msg.state.linear.z = 1;
        state_msg.state.angular.x = 1;
        state_msg.state.angular.y = 1;
        state_msg.state.angular.z = 1;
        state_msg.state.linear.x = 1;
        state_msg.state.linear.y = 1;
        state_msg.state.linear.z = 1;
        state_msg.state.angular.x = 1;
        state_msg.state.angular.y = 1;
        state_msg.state.angular.z = 1;


        ROS_INFO("State vector sent (state publisher): z=%f", state_msg.state.linear.z);

        state_pub.publish(state_msg);


        ros::spinOnce();

        loop_rate.sleep();
      }


    return 0;
}
