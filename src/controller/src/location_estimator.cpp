/**
 * Fusion of the data from : gps_localization
 *                           imu_localization
 *                           sounder_localization
 *
 */

#include "ros/ros.h"
#include "std_msgs/Float64.h"
#include "msgs_pkg/State_vector.h"
#include "geometry_msgs/Twist.h"
#include "geometry_msgs/Vector3.h"


// Publish data as merged_pos_msg
// Publishing also data received by the regulator as state_msg


void imuCallback(const std_msgs::String::ConstPtr& msg) {
	//ROS_INFO("I heard: [%s]", msg->data.c_str());
}

void gpsCallback(const geometry_msgs::Vector3::ConstPtr& msg) {
	//ROS_INFO("I heard: [%s]", msg->data.c_str());
}


int main(int argc, char **argv) {
    ros::init(argc, argv, "location_estimator");
    ros::NodeHandle n;
    
    // Publish state vector estimation:
    ros::Publisher state_pub_relayed = n.advertise<msgs_pkg::State_vector>("state_vector_relayed", 1000);
    msgs_pkg::State_vector state_relayed_msg;

    // Publish merged position:
    ros::Publisher merged_pos_msg = n.advertise<geometry_msgs::Twist>("merged_position", 1000);
    geometry_msgs::Twist merged_pos;

    ros::Rate loop_rate(10);

    while (ros::ok()) {

    	// --------------- Subscribing -----------------
        ros::Subscriber imu_sub = n.subscribe("gps_position", 1000, imuCallback);

		ros::Subscriber gps_sub = n.subscribe("imu_localization", 1000, gpsCallback);


    	// --------------- Processing -----------------
        // Merged position: - The imu is the only one giving the orientation, so we take it !
        merged_pos.angular = ;  // the imu's result


        // Basic test for the localization: TODO
        if (gps_position.ok) {  // change it
        	merged_pos.linear = gps_position.linear;
        	merged_pos.linear.z = 0;  // To be sure we are at the surface
        } else {
        	merged_pos.linear = ;  // result of the fusion
        }


		// --------------- Logs -----------------
        // ROS_INFO("State vector sent (state publisher): z=%f", state_msg.state.linear.z);


    	// --------------- Publishing -----------------
        // State_relayed:
        state_pub_relayed.publish(state_relayed_msg);

        // Merged pos
        merged_pos_msg.publish(merged_pos);


    	// --------------- End of the loop -----------------
        ros::spinOnce();

        loop_rate.sleep();
    }
    return 0;
}