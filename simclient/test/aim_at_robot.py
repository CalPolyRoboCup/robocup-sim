from simclient.command import Command, CommandStatus
from simclient.math.vector2 import Vector2
from simclient.math.math_helper import MathHelper
from simclient.master import Master


class AimAtRobot(Command):
    """
    The AimAtRobot command is used for positioning the robot so the ball lies between this robot and the target robot
    """

    ORBIT_RADIUS = 240.0
    VELOCITY_THRESHOLD = 0.005
    MAXIMUM_DISTANCE = 5.0

    def __init__(self, master: Master, target_robot_id: int):
        """
        Initializes a new AimAtRobot instance
        :param master: The master instance
        :param target_robot_id: The ID of the robot to target
        """
        super().__init__(master)
        self.target_robot_id = target_robot_id
        self.target_robot = None
        self.target_pos = Vector2()

    def assigned(self):
        """
        Not implemented
        """
        pass

    def start(self):
        """
        Sets the initial default target position to 0, 0
        """
        self.target_pos.set(0, 0)

    def update(self, delta_time: float):
        """
        Updates the robot outputs
        :param delta_time: The time passed since the last update
        """
        if self.target_robot is None:
            # If the robot has not been detected, refresh
            self.target_robot = self.team_bots.robots[self.target_robot_id]
            return

        # Get the robot and ball positions
        robot_pos = self.get_robot().transform.position
        ball_pos = self.ball.position

        # Point the robot directly at the ball
        target_orientation = MathHelper.get_line_angle(robot_pos, ball_pos)
        self.get_robot().set_target_orientation(target_orientation)

        # Identify the final target position (so the ball lies in between this robot and the target)
        target_robot_pos = self.target_robot.transform.position
        self.target_pos = ball_pos + (ball_pos - target_robot_pos).normalized() * AimAtRobot.ORBIT_RADIUS

        # Set the speed of the robot according to how far it is from the target
        self.get_robot().set_target_speed(min((robot_pos - self.target_pos).length() *
                                              AimAtRobot.VELOCITY_THRESHOLD, 1.0))

        # Initialize the current target position to the final target position
        current_target_pos = self.target_pos

        if (robot_pos - current_target_pos).length() > AimAtRobot.ORBIT_RADIUS:
            # If the robot is far away from the target, move its path to avoid hitting the ball
            current_target_pos = ball_pos - (ball_pos - MathHelper.get_closest_point(
                robot_pos, current_target_pos, ball_pos)).normalized() * AimAtRobot.ORBIT_RADIUS

        # Set the robot's direction toward the target
        target_direction = -MathHelper.get_line_angle(robot_pos, current_target_pos)
        self.get_robot().set_target_direction(target_direction)

    def get_status(self) -> CommandStatus:
        """
        Returns the current status of the command
        :return: The current status of the command
        """
        if (self.get_robot().transform.position - self.target_pos).length() < AimAtRobot.MAXIMUM_DISTANCE:
            # If we have reached the target position, we are done
            return CommandStatus.COMPLETED

        # Otherwise, we're still running
        return CommandStatus.RUNNING

    def interrupted(self):
        """
        Not implemented
        """
        pass

    def end(self, command_status: CommandStatus):
        """
        Sets the target speed to zero when the command is finished
        """
        self.get_robot().set_target_speed(0)
