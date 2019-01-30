from simclient.command import Command, CommandStatus
from simclient.math.math_helper import MathHelper


class StayPut(Command):
    """
    Makes the robot stay in the same position
    """
    VELOCITY_THRESHOLD = 0.005

    def __init__(self, master):
        """
        Initializes a new StayPut instance
        :param master: The Master instance
        """
        super().__init__(master)
        self.start_position = None

    def assigned(self):
        """
        Not implemented
        """
        pass

    def start(self):
        """
        Initializes the robot's initial position
        """
        if self.start_position is None:
            self.start_position = self.get_robot().transform.position.copy()

    def update(self, delta_time: float):
        """
        Updates this command
        :param delta_time: The time since the last update
        """
        robot = self.get_robot()
        robot_pos = robot.transform.position

        # Set the target speed so it moves back to the ball without overshooting
        robot.set_target_speed(min((robot_pos - self.start_position).length() * StayPut.VELOCITY_THRESHOLD, 1.0))

        # Sets the direction of the robot toward its starting position
        target_direction = -MathHelper.get_line_angle(robot_pos, self.start_position)
        robot.set_target_direction(target_direction)

        ball_pos = self.ball.position

        # Set the orientation to be facing toward the ball
        target_orientation = MathHelper.get_line_angle(robot_pos, ball_pos)
        robot.set_target_orientation(target_orientation)

    def get_status(self) -> CommandStatus:
        """
        This command runs indefinitely
        :return: The status of the command (will always be RUNNING)
        """
        return CommandStatus.RUNNING

    def end(self, command_status: CommandStatus):
        """
        Not implemented
        """
        pass
