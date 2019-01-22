import math

import pygame

from proto.messages_robocup_ssl_detection_pb2 import SSL_DetectionRobot

from simclient.team import Team
from simclient.util.vector2 import Vector2


class RobotTransform:
    """
    Contains position and orientation information for a robot
    """
    def __init__(self):
        """
        Initializes a new RobotTransform instance
        """
        self.position = Vector2()
        self.orientation = 0

    def set(self, position: Vector2, orientation: float):
        """
        Sets the position and orientation properties from the given position and orientation arguments
        :param position: The new position value
        :param orientation: The new orientation value
        """
        self.position.copy_from(position)
        self.orientation = orientation

    def decode(self, det_robot: SSL_DetectionRobot):
        """
        Decodes an SSL_DetectionRobot packet and updates the transform information accordingly
        :param det_robot: The SSL_DetectionRobot packet to decode
        """
        self.position.set(det_robot.x, det_robot.y)
        self.orientation = det_robot.orientation

    def copy_from(self, transform: 'RobotTransform'):
        """
        Copies the transform information from a RobotTransform into this instance
        :param transform: The RobotTransform from which to update this transform information
        """
        self.position.copy_from(transform.position)
        self.orientation = transform.orientation

    def __eq__(self, other):
        """
        Checks equality between this and another instance
        :param other: The other RobotTransform
        :return: True if both instances are equal, otherwise False
        """
        return other is RobotTransform and self.position == other.position and other.orientation == self.orientation


class Robot:
    """
    Decodes and renders robot packets from grSim, and manages commands to send back to grSim for a specific robot
    """
    RADIUS = 90
    OUTLINE_SIZE = 1
    YELLOW_TEAM_COLOR = (255, 255, 0)
    BLUE_TEAM_COLOR = (0, 0, 255)

    def __init__(self, team: Team, det_robot: SSL_DetectionRobot):
        """
        Initialize a new Robot instance
        :param team: The team the robot is on
        :param det_robot: The SSL_DetectionRobot packet used to initialize robot information
        """
        self.color = Robot.YELLOW_TEAM_COLOR if team == Team.YELLOW else Robot.BLUE_TEAM_COLOR
        self.id = det_robot.robot_id
        self.last_transform = RobotTransform()
        self.last_transform.decode(det_robot)
        self.transform = RobotTransform()
        self.speed = 0
        self.direction = 0
        self.angular_velocity = 0

    def decode(self, det_robot: SSL_DetectionRobot):
        """
        Decodes an SSL_DetectionRobot packet
        :param det_robot: The SSL_DetectionRobot packet from which to update
        """
        self.transform.decode(det_robot)

    def update(self, delta_time: float):
        """
        Updates transform velocity information
        :param delta_time: The time passed since the last update
        """
        if self.transform != self.last_transform:
            # If the robot has moved since the last frame, update velocity information
            self.speed = self.transform.position.subtract(self.last_transform.position).length() / delta_time * 0.001

            if self.speed > 0:
                self.direction = math.atan2(self.transform.position.y - self.last_transform.position.y,
                                            self.transform.position.x - self.last_transform.position.x)

            self.angular_velocity = (self.transform.orientation - self.last_transform.orientation) / delta_time

            self.last_transform.copy_from(self.transform)

    def render(self, client):
        """
        Render the robot to the given client
        :param client: The client which to render the robot
        """
        # Draw the filled circle of the robot
        pygame.draw.circle(client.screen, self.color,
                           client.screen_point(self.transform.position.x, self.transform.position.y),
                           client.screen_scalar(Robot.RADIUS))

        # Draw the outline of the robot
        pygame.draw.circle(client.screen, (0, 0, 0),
                           client.screen_point(self.transform.position.x, self.transform.position.y),
                           client.screen_scalar(Robot.RADIUS) + Robot.OUTLINE_SIZE, Robot.OUTLINE_SIZE)
