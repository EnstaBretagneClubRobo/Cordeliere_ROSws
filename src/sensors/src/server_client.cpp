#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <sys/socket.h>
#include <arpa/inet.h>
#include <signal.h>
#include <ros/ros.h>
#include <msgs_pkg/3DBox.h>
#include <msgs_pkg/Interval.h>

int socket_RV;
msgs_pkg::3DBox box_out;
msgs_pkg::Interval Z_in;

void signals_handler(int signal_number)
{
	close(socket_RV);
	fflush(stdout);
	printf("\nClosed cleanly\n");
}

void client(char* IP, int port)
{
	struct sockaddr_in adr;

	if( (socket_RV=socket(AF_INET, SOCK_STREAM, 0)) == -1 )
	{
		perror("Socket RV failure");
		exit(1);
	}
	
	adr.sin_addr.s_addr = inet_addr(IP);
	adr.sin_family = AF_INET;
	adr.sin_port = htons(port);

	if ( connect(socket_RV,(struct sockaddr *)&adr, sizeof(adr))==-1 )
	{
		perror("Connection failure");
		exit(1);
	}

}


void send_to ()
{
	ros::Rate loop_rate(10);
	char buffer[500];

	sprintf(buffer,"$Z_sent,%lf,%lf,%lf\n",ros::Time::now().toSec(), Z_in.lb, Z_in.ub, 100.0);

	if( send(socket_service, buffer, strlen(buffer), 0) < 0 )
	{
		printf("End of connection\n");
		break;
	}

	// send z_interval
	ros::spinOnce();
    loop_rate.sleep();

}

void rec_from ()
{
	ros::Rate loop_rate(10);
	char c[1];
	string rcv_msg;
	string delimiter = ",";
	int res;
	int i, j;
	
	do{
		res = recv(socket_service, c, 1, 0);

		if( res <= 0 )
		{
			printf("End of connection\n");
			break;
		}
		
		rcv_msg.append(c);
	} while((int)c[0] != 0);

	// Parser to get the computed box from tcp server
	// Received message is assumed to be: xlb,xub,ylb,yub,zlb,zub
	size_t pos = 0;
	int compt = 0;
	std::string token;
	while ((pos = rcv_msg.find(delimiter)) != std::string::npos) {
			token = rcv_msg.substr(0, pos);
		std::cout << token << std::endl;
		switch (compt)
		{
    		case 0:
    		box_out.X.lb = stof(token);
    		case 1:
    		box_out.X.ub = stof(token);
    		case 2:
    		box_out.Y.lb = stof(token);
    		case 3:
    		box_out.Y.ub = stof(token);
    		case 4:
    		box_out.Z.lb = stof(token);
    		case 5:
    		box_out.Z.ub = stof(token);
    	}
		//s.erase(0, pos + delimiter.length());
	}
	//std::cout << s << std::endl;
	printf("Recv : %s\n", rcv_msg.c_str());
	// Publish the box computed by the localisation algorithm:
	contracted_box.publish(box_out);
	rcv_msg.clear();

}

void posCallback(const std_msgs::Float64::ConstPtr& msg){
	Z_in.ub = msg->data;
}

void distCallback(const std_msgs::Float64::ConstPtr& msg){
	Z_in.lb = msg->data;
}

int main(int argc, char *argv[]) {

	// Check correct use and update parameters
    if (argc != 4)
    {
        printf("Listen on a TCP server.\nNeeded 3 arguments but %d given.\nUse this way -> ./listener IP Port Message\n", argc-1);
        return EXIT_FAILURE;
    }

	// SIGACTION
    struct sigaction action;

    action.sa_handler = signals_handler;
    sigemptyset(& (action.sa_mask));

    sigaction(SIGQUIT, & action, NULL);
    sigaction(SIGINT, & action, NULL);
    // END SIGACTION

	ros::init(argc, argv, "tcp_client");
    ros::NodeHandle n;
    ros::Publisher contracted_box = n.advertise<msgs_pkg::3DBox>("contracted_box", 1000);
    ros::Subscriber pressure_meter_listener = n.subscribe("pressure_meter_chatter", 1000, posCallback);
    ros::Subscriber sounder_listener = n.subscribe("distance_to_depth", 1000, distCallback);

    // Server client
    client(argv[1], atoi(argv[2]));

    // Init msg


    // Loop
    while (ros::ok()){
    	send_to();
    	rec_from();
    }



    // Send message
	send(socket_RV, argv[3], strlen(argv[3]), 0);

	close(socket_RV);

	return EXIT_SUCCESS;
}
