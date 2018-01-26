#include "ros/ros.h"
#include "std_msgs/Float64.h"
#include "msgs_pkg/State_vector.h"
#include "geometry_msgs/Twist.h"


// Publish the state vector estimation in the "state_vector" topic.

int main(int argc, char **argv)
{
    ros::init(argc, argv, "state_vector_publisher");
    ros::NodeHandle n;
    
    // Publish state vector estimation.
    ros::Publisher state_pub = n.advertise<msgs_pkg::State_vector>("state_vector", 1000);
    msgs_pkg::State_vector state_msg;

    // Publish command
    ros::Publisher command_pub = n.advertise<geometry_msgs::Twist>("command", 1000);
    geometry_msgs::Twist command_msg

    ros::Rate loop_rate(10);

    while (ros::ok())
      {
        // State vector values:
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

        // Command Values:
        command_msg.linear.x = 1;  // TODO: compute it
        command_msg.linear.y = 0;
        command_msg.linear.z = 0;
        command_msg.angular.x = 0;  // TODO: compute it
        command_msg.angular.y = 0;  // TODO: compute it
        command_msg.angular.z = 0;  // TODO: compute it


        state_pub.publish(state_msg);
        // ROS_INFO("State vector sent (state publisher): z=%f", state_msg.state.linear.z);

        command_pub.publish(command_msg);
        ROS_INFO("Command vector sent (state publisher): phi=%f", command_msg.angular.x);
        ROS_INFO("Command vector sent (state publisher): theta=%f", command_msg.angular.y);
        ROS_INFO("Command vector sent (state publisher): psi=%f", command_msg.angular.z);


        ros::spinOnce();

        loop_rate.sleep();
      }


    return 0;
}
