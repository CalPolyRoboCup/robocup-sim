import math

from simclient.command import Command, CommandStatus
from simclient.util.math_helper import MathHelper


class LineUpPass(Command):
    """
    Lines up with the ball to pass to another robot
    """
    TARGET_DISTANCE = 90
    VELOCITY_THRESHOLD = 0.005
    MAXIMUM_DISTANCE = 110
    MAXIMUM_ANGLE = math.pi * 0.25

    def __init__(self, master, target_robot):
        """
        Initializes a new LineUpPass instance
        :param master: The Master instance
        :param target_robot: The target robot to pass to
        """
        super(LineUpPass, self).__init__(master)
        self.target_robot_id = target_robot
        self.target_robot = None
        self.target_orientation = 0.0
        self.target_direction = 0.0

    def assigned(self):
        """
        Not implemented
        """
        pass

    def start(self):
        """
        Resets the target orientation and direction
        """
        self.target_orientation = 0.0
        self.target_direction = 0.0

    def update(self, delta_time):
        """
        Updates the logic for lining up the pass
        :param delta_time: The time passed since the last update
        """
        # If the next robot is not detected, don't do anything this frame
        if self.target_robot is None:
            self.target_robot = self.team_bots.robots[self.target_robot_id]
            return

        # Get robot information
        robot = self.get_robot()
        robot_pos = robot.transform.position
        target_robot_pos = self.target_robot.transform.position

        # Set the target orientation to face toward the target robot
        self.target_orientation = MathHelper.get_line_angle(robot_pos, target_robot_pos)
        robot.set_target_orientation(self.target_orientation)

        # Get the ball's position
        ball_pos = self.ball.position

        # Set the speed of the robot to approach the ball carefully
        robot.set_target_speed(min(max(((robot_pos - ball_pos).length() -
                                        LineUpPass.TARGET_DISTANCE) * LineUpPass.VELOCITY_THRESHOLD, 0.0), 1.0))

        # Set the direction of the robot to move toward the ball
        self.target_direction = -MathHelper.get_line_angle(robot_pos, ball_pos)
        robot.set_target_direction(self.target_direction)

    def get_status(self):
        """
        Returns the current status of the command
        :return: The current status of the command
        """
        if (self.get_robot().transform.position - self.ball.position).length() < LineUpPass.MAXIMUM_DISTANCE:
            # If we've reached the ball, we're finished
            return CommandStatus.COMPLETED

        if abs(abs(self.target_orientation) - abs(self.target_direction)) > LineUpPass.MAXIMUM_ANGLE:
            # If the ball has been knocked out of the way, we've failed
            return CommandStatus.FAILED

        # If none of the above conditions were met, we're still running
        return CommandStatus.RUNNING

    def end(self, command_status):
        pass


Command.register(LineUpPass)