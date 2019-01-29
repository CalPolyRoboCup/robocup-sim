import math

import logging

import pygame

from proto.messages_robocup_ssl_detection_pb2 import SSL_DetectionRobot
from proto.grSim_Commands_pb2 import grSim_Robot_Command

from simclient.command import CommandStatus
from simclient.team import Team
from simclient.math.vector2 import Vector2
from simclient.math.pid import PID
from simclient.math.math_helper import MathHelper


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
    ORIENTATION_P = 10.0
    ORIENTATION_I = 0.0
    ORIENTATION_D = 0.25
    MAX_ANGULAR_OUT = math.pi * 4
    OUTLINE_SIZE = 1
    KICKER_THICKNESS = 30
    KICKER_WIDTH = 0.6
    KICKER_OFFSET = 10
    KICKER_COLOR = (127, 127, 127)
    YELLOW_TEAM_COLOR = (255, 255, 0)
    BLUE_TEAM_COLOR = (0, 0, 255)

    def __init__(self, team: Team, det_robot: SSL_DetectionRobot):
        """
        Initialize a new Robot instance
        :param team: The team the robot is on
        :param det_robot: The SSL_DetectionRobot packet used to initialize robot information
        """
        self.logger = logging.getLogger(__name__)
        self.color = Robot.YELLOW_TEAM_COLOR if team == Team.YELLOW else Robot.BLUE_TEAM_COLOR
        self.id = det_robot.robot_id
        self.last_transform = RobotTransform()
        self.last_transform.decode(det_robot)
        self.transform = RobotTransform()
        self.screen_pos = Vector2()
        self.speed = 0
        self.direction = 0
        self.angular_velocity = 0

        self._default_command = None
        self._waiting_command = None
        self._command = None
        self._target_speed = 0.0
        self._target_direction = 0.0
        self._target_orientation = 0.0
        self._target_angular_velocity = 0.0
        self._kicker_speed = 0.0
        self._orientation_pid = PID(Robot.ORIENTATION_P, Robot.ORIENTATION_I, Robot.ORIENTATION_D,
                                    -Robot.MAX_ANGULAR_OUT, Robot.MAX_ANGULAR_OUT)

    def set_target_speed(self, speed: float):
        """
        Sets the target speed of the robot
        :param speed: The speed of the robot
        """
        self._target_speed = speed

    def set_target_direction(self, angle: float):
        """
        Sets the target direction of the robot
        :param angle: The direction of the robot in radians
        """
        self._target_direction = angle

    def set_target_orientation(self, angle: float):
        """
        Sets the target orientation of the robot
        :param angle: The orientation of the robot in radians
        """
        self._target_orientation = angle

        # Normalize the angle
        while angle < 0:
            angle += math.pi * 2

        while angle > math.pi * 2:
            angle -= math.pi * 2

        # Update the orientation PID set point
        self._orientation_pid.set_point = angle

    def set_kicker_speed(self, speed: float):
        """
        Sets the kicker speed of the robot
        :param speed: The speed to set the kicker
        """
        self._kicker_speed = speed

    def write_output(self, robot_command: grSim_Robot_Command):
        """
        Populates the given grSim_Robot_Command with the current outputs
        :param robot_command: The grSim_Robot_Command to populate
        """
        robot_command.id = self.id

        # We don't set wheel speeds individually, so fill these out with zeros
        robot_command.wheelsspeed = False
        robot_command.wheel1 = 0.0
        robot_command.wheel2 = 0.0
        robot_command.wheel3 = 0.0
        robot_command.wheel4 = 0.0

        # Fill out velocity information
        robot_command.veltangent = self._target_speed * math.cos(self._target_direction + self.transform.orientation)
        robot_command.velnormal = -self._target_speed * math.sin(self._target_direction + self.transform.orientation)
        robot_command.velangular = self._target_angular_velocity

        # Fill out kicker information
        robot_command.kickspeedx = self._kicker_speed
        robot_command.kickspeedz = 0.0
        robot_command.spinner = False

    def set_default_command(self, command):
        """
        Sets the robot's default command - the command will be executed if all other commands have terminated
        :param command: The command to be defined as the default
        """
        if command.get_robot() == self or command.set_robot(self):
            self._default_command = command
        else:
            self.logger.log(logging.WARNING, "Cannot set a default Command that's already been assigned"
                                             "to another Robot!")

    def run_command(self, command):
        """
        Runs the given command on the robot
        :param command: The command to run on the robot
        """
        if command.get_robot() == self or command.set_robot(self):
            self._waiting_command = command
        else:
            self.logger.log(logging.WARNING, "Cannot run a Command that's already been assigned to"
                                             "another robot!")

    def decode(self, det_robot: SSL_DetectionRobot):
        """
        Decodes an SSL_DetectionRobot packet
        :param det_robot: The SSL_DetectionRobot packet from which to update
        """
        self.transform.decode(det_robot)

    def update_stats(self, delta_time: float):
        """
        Updates transform velocity information
        :param delta_time: The time passed since the last update
        """
        if self.transform != self.last_transform:
            # If the robot has moved since the last frame, update velocity information
            self.speed = (self.transform.position - self.last_transform.position).length() / delta_time * 0.001

            if self.speed > 0:
                self.direction = math.atan2(self.transform.position.y - self.last_transform.position.y,
                                            self.transform.position.x - self.last_transform.position.x)

            self.angular_velocity = (self.transform.orientation - self.last_transform.orientation) / delta_time

            self.last_transform.copy_from(self.transform)

    def update_command(self, delta_time: float):
        """
        Checks to see if there are any state changes to the active command, then updates the current command
        :param delta_time: The time passed since the last update
        """
        if self._waiting_command is not None:
            # If a new command is waiting to be executed, interrupt any current commands and start execution of
            # the new one
            if self._command is not None:
                self._command.interrupted()
                self._command.end(CommandStatus.FAILED)

            self._command = self._waiting_command
            self._waiting_command = None
            self._command.start()

        if self._command is not None:
            # Update the current command if valid
            status = self._command.get_status()

            if status == CommandStatus.RUNNING:
                self._command.update(delta_time)
            else:
                self._command.end(status)
                self._command = None

        if self._command is None and self._waiting_command is None and self._default_command is not None:
            # If there is not command running and no commands are waiting, run the default command
            self._command = self._default_command
            self._command.start()

        # Update the target angular velocity using PID
        self._target_angular_velocity = self._orientation_pid.calculate(delta_time, MathHelper.adjust_angle_value(
            self._orientation_pid.set_point, self.transform.orientation))

    def render(self, master):
        """
        Render the robot to the given master's window
        :param master: The master which to render the robot
        """
        # Calculate and update position on screen
        screen_point = master.screen_point(self.transform.position.x, self.transform.position.y)
        self.screen_pos.set(screen_point[0], screen_point[1])

        # Draw the filled circle of the robot
        pygame.draw.circle(master.screen, self.color, screen_point, master.screen_scalar(Robot.RADIUS))

        # Draw the outline of the robot
        pygame.draw.circle(master.screen, (0, 0, 0), screen_point, master.screen_scalar(Robot.RADIUS),
                           Robot.OUTLINE_SIZE)

        # Draw the kicker of the robot
        pygame.draw.line(master.screen, Robot.KICKER_COLOR,
                         master.screen_point(self.transform.position.x + (Robot.RADIUS + Robot.KICKER_OFFSET) *
                                             math.cos(self.transform.orientation + Robot.KICKER_WIDTH),
                                             self.transform.position.y + Robot.RADIUS *
                                             math.sin(self.transform.orientation + Robot.KICKER_WIDTH)),
                         master.screen_point(self.transform.position.x + (Robot.RADIUS + Robot.KICKER_OFFSET) *
                                             math.cos(self.transform.orientation - Robot.KICKER_WIDTH),
                                             self.transform.position.y + Robot.RADIUS *
                                             math.sin(self.transform.orientation - Robot.KICKER_WIDTH)),
                         master.screen_scalar(Robot.KICKER_THICKNESS))
