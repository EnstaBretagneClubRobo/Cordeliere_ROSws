#include "ros/ros.h"

#include "geometry_msgs/Twist.h"
#include "msgs_pkg/State_vector.h"
#include "geometry_msgs/Twist.h"

// Extract mission from file

void extractMission() {
    ROS_INFO("Still to implement\n");
}

// Compute the commands in order to follow waypoints.

void regulation()
{
    ROS_INFO("Still to implement\n");
}

// Callback method for subscribing

void chatCallback(const geometry_msgs::Twist::ConstPtr& msg)
{
    ROS_INFO("Still to implement\n");
}

// Publish the state vector estimation in the "state_vector" topic.

int main(int argc, char **argv)
{
    // Initialization of the node
    ros::init(argc, argv, "state_vector_publisher");
    ros::NodeHandle n;
  
    ros::Rate loop_rate(10);

    // Initialization of messages/services
    ros::Publisher state_pub    = n.advertise<msgs_pkg::State_vector>("state_vector", 1000);
    msgs_pkg::State_vector state_msg;


    ros::Publisher cmd_pub      = n.advertise<msgs_pkg::Command>("Command", 1000);
    msgs_pkg::State_vector command_msg;

    ros::Subscriber none_sub    = n.subscribe("none", 1000, chatCallback);

    while (ros::ok())
      {
        /**
         * Compute commands
         */

        regulation();

        /**
         * Publish state vector estimation.
         */

        // Values
        state_msg.state.linear.x    = 1;
        state_msg.state.linear.y    = 1;
        state_msg.state.linear.z    = 1;
        state_msg.state.angular.x   = 1;
        state_msg.state.angular.y   = 1;
        state_msg.state.angular.z   = 1;

        state_msg.dot_state.linear.x  = 1;
        state_msg.dot_state.linear.y  = 1;
        state_msg.dot_state.linear.z  = 1;
        state_msg.dot_state.angular.x = 1;
        state_msg.dot_state.angular.y = 1;
        state_msg.dot_state.angular.z = 1;


        state_pub.publish(state_msg);
        // ROS_INFO("State vector sent (state publisher): z=%f", state_msg.state.linear.z);

        command_pub.publish(command_msg);
        ROS_INFO("Command vector sent (state publisher): phi=%f", command_msg.angular.x);
        ROS_INFO("Command vector sent (state publisher): theta=%f", command_msg.angular.y);
        ROS_INFO("Command vector sent (state publisher): psi=%f", command_msg.angular.z);

        /**
         * Publish new commands.
         */

        // Values
        command_msg.vertical.throttle   = 1;
        command_msg.vertical.balance    = 1;
        command_msg.horizontal.throttle = 1;
        command_msg.horizontal.balance  = 1;

        cmd_pub.publish(command_msg);


        ros::spinOnce();

        loop_rate.sleep();
      }


    return 0;
}
