from proto.messages_robocup_ssl_detection_pb2 import SSL_DetectionRobot

from simclient.robot import Robot
from simclient.team import Team


class RobotManager:
    """
    Manages and updates a team of robots
    """
    def __init__(self, team: Team):
        """
        Initializes a new RobotManager instance
        :param team: The team that the RobotManager is managing
        """
        self.team = team
        self.robots = []

    def decode(self, det_robots: [SSL_DetectionRobot]):
        """
        Decode a list of SSL_DetectionRobot packets and update the managed robots accordingly
        :param det_robots: The list of SSL_DetectionRobot packets to decode
        """
        for robot in det_robots:
            for i in range(len(self.robots), robot.robot_id + 1):
                # If more robots were added, expand the list of robots
                self.robots.append(None)

            if self.robots[robot.robot_id] is None:
                # if a robot hasn't been updated yet, create a new robot instance
                self.robots[robot.robot_id] = Robot(self.team, robot)

            # Decode the current SSL_DetectionRobot packet
            self.robots[robot.robot_id].decode(robot)

    def update(self, delta_time: float):
        """
        Update all team robots
        :param delta_time: The time passed since the last update
        """
        for robot in self.robots:
            if robot is not None:
                robot.update(delta_time)

    def render(self, client):
        """
        Renders all team robots to the client
        :param client: The client which to render the robots
        """
        for robot in self.robots:
            if robot is not None:
                robot.render(client)
