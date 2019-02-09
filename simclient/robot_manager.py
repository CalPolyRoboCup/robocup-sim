from proto.messages_robocup_ssl_detection_pb2 import SSL_DetectionRobot

from simclient.robot import Robot
from simclient.team import Team


class RobotManager:
    """
    Manages and updates a team of robots
    """

    DEFAULT_TEAM_SIZE = 12

    def __init__(self, team):
        """
        Initializes a new RobotManager instance
        :param team: The team that the RobotManager is managing
        """
        self.team = team
        self.robots = RobotManager.DEFAULT_TEAM_SIZE * [None]

    def decode(self, det_robots, init_robot):
        """
        Decode a list of SSL_DetectionRobot packets and update the managed robots accordingly
        :param det_robots: The list of SSL_DetectionRobot packets to decode
        :param init_robot: Called if a new robot is detected
        """
        for robot in det_robots:
            for i in range(len(self.robots), robot.robot_id + 1):
                # If more robots were added, expand the list of robots
                self.robots.append(None)

            if self.robots[robot.robot_id] is None:
                # if a robot hasn't been updated yet, create a new robot instance
                new_robot = self.robots[robot.robot_id] = Robot(self.team, robot)
                init_robot(new_robot)

            # Decode the current SSL_DetectionRobot packet
            self.robots[robot.robot_id].decode(robot)

    def update_stats(self, delta_time):
        """
        Update all team robots
        :param delta_time: The time passed since the last update
        """
        for robot in self.robots:
            if robot is not None:
                robot.update_stats(delta_time)

    def update_commands(self, delta_time):
        """
        Update each command on each robot
        :param delta_time: The time passed since the last update
        """
        for robot in self.robots:
            if robot is not None:
                robot.update_command(delta_time)

    def write_output(self, robot_commands):
        """
        Write each robot's outputs to the given command packet
        :param robot_commands: The command packet to be updated
        """
        for robot in self.robots:
            if robot is not None:
                robot.write_output(robot_commands.add())

    def render(self, master):
        """
        Renders all team robots to the master's window
        :param master: The master which to render the robots
        """
        for robot in self.robots:
            if robot is not None:
                robot.render(master)
