#include <iostream>
#include <QUdpSocket>
#include "messages_robocup_ssl_wrapper.pb.h"

namespace{
	const int myRobotId = 6;
	const int vision_port = 10076;
	//QUdpSocket sendSocket;
    QUdpSocket receiveSocket;
	struct Robot{
		Robot() :id(-1), x(-9999), y(-9999), orientation(-9999) {}
		int id;
		double x;
		double y;
		double orientation;
	};
	Robot myRobot[12];
}

using namespace std;

void set_up(){
	receiveSocket.bind(QHostAddress::AnyIPv4, vision_port, QUdpSocket::ShareAddress);
    receiveSocket.joinMulticastGroup(QHostAddress("224.5.23.2"));
}

void run_loop(){
	while(true){
		QByteArray datagram;
	    while (receiveSocket.state() == QUdpSocket::BoundState && receiveSocket.hasPendingDatagrams()) {
	        datagram.resize(receiveSocket.pendingDatagramSize());
			receiveSocket.readDatagram(datagram.data(), datagram.size());

			SSL_WrapperPacket packet;
			packet.ParseFromArray(datagram.data(), datagram.size());
			const auto detection = packet.detection();
			const auto camID = detection.camera_id();
			const auto blueSize = detection.robots_blue_size();
			const auto yellowSize = detection.robots_yellow_size();
			
			for (int i = 0; i < blueSize; i++) {
	            const auto robot = detection.robots_blue(i);
				int id = robot.robot_id();
				myRobot[id].x = robot.x();
				myRobot[id].y = robot.y();
				myRobot[id].orientation = robot.orientation();
	        }
			cout << myRobot[6].x << ", " << myRobot[6].y  << ", " << myRobot[6].orientation << endl;
	    }
	}
}

int main(){
	set_up();
	run_loop();
	return 0;
}