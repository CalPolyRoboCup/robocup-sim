import math

from simclient.command import Command, CommandStatus

from simclient.math.vector2 import Vector2
from simclient.math.math_helper import MathHelper


class CatchBall(Command):
    """
    Catches a pass from another robot
    """
    VELOCITY_THRESHOLD = 0.01
    BALL_VELOCITY_THRESHOLD = 0.005
    MAXIMUM_DISTANCE = 130

    def __init__(self, master):
        """
        Initializes a new CatchBall instance
        :param master: The master instance
        """
        super().__init__(master)
        self.ball_direction_vector = Vector2()

    def assigned(self):
        """
        Not implemented
        """
        pass

    def start(self):
        """
        Not implemented
        """
        pass

    def update(self, delta_time: float):
        """
        Updates the catch ball logic
        :param delta_time: The time passed since the last update
        """
        # Get robot and ball information
        robot = self.get_robot()
        robot_pos = robot.transform.position
        ball_pos = self.ball.position

        # Calculate and store the ball's direction
        ball_direction = self.ball.direction
        self.ball_direction_vector.set(math.cos(ball_direction), -math.sin(ball_direction))

        # Make the robot face against the ball's direction
        robot.set_target_orientation(math.atan2(self.ball_direction_vector.y, self.ball_direction_vector.x) + math.pi)

        # Set the target point to the closest point moving only perpendicular to the ball's motion
        target_pos = MathHelper.get_closest_point(ball_pos, ball_pos + self.ball_direction_vector, robot_pos)

        # Set the target direction toward the target position
        target_direction = -MathHelper.get_line_angle(robot_pos, target_pos)

        # Write target values to the robot
        robot.set_target_direction(target_direction)
        robot.set_target_speed(min((robot_pos - target_pos).length() * CatchBall.VELOCITY_THRESHOLD, 1.0))

    def get_status(self) -> CommandStatus:
        """
        Returns the current status of the command
        :return: The current status of the command
        """
        if self.ball.speed < CatchBall.BALL_VELOCITY_THRESHOLD or \
                (self.ball.position + self.ball_direction_vector * 0.001 -
                 self.get_robot().transform.position).length() > \
                (self.ball.position - self.get_robot().transform.position).length():
            # If the ball has stopped moving, or is moving away from the robot, we have failed to catch the ball
            return CommandStatus.FAILED

        # If we have made contact with the ball, we have finished
        if (self.get_robot().transform.position - self.ball.position).length() < CatchBall.MAXIMUM_DISTANCE:
            return CommandStatus.COMPLETED

        # If none of the above cases occurred, we're still running
        return CommandStatus.RUNNING

    def end(self, command_status: CommandStatus):
        """
        When this command completes, make the robot pass to the next robot
        :param command_status: The status that made this command terminate
        """
        # Make the robot stop moving
        self.get_robot().set_target_speed(0.0)

        # Find the next valid robot
        i = self.get_robot().id + 1
        next_robot = None

        while next_robot is None:
            next_robot = self.team_bots.robots[i % len(self.team_bots.robots)]
            i += 1

        # Pass to the next robot
        from .pass_to_robot import PassToRobot
        self.get_robot().run_command(PassToRobot(self.master, next_robot.id))
        del PassToRobot
