from simclient.command_series import CommandSeries, CommandStatus, FailResponse

from simclient.test.aim_at_robot import AimAtRobot
from simclient.test.line_up_pass import LineUpPass

from simclient.commands.set_kicker import SetKicker
from simclient.commands.delay import Delay


class PassToRobot(CommandSeries):
    """
    Passes the ball to the indicated robot
    """
    def __init__(self, master, target_robot_id):
        """
        Initializes a new PassToRobot instance
        :param master: The master instance
        :param target_robot_id: The ID of the robot to pass to
        """
        super(PassToRobot, self).__init__(master)

        self.target_robot_id = target_robot_id

        self.add_command(AimAtRobot(master, target_robot_id))
        self.add_command(LineUpPass(master, target_robot_id), FailResponse.FAIL)
        self.add_command(SetKicker(master, 4.0))
        self.add_command(Delay(master, 0.05))
        self.add_command(SetKicker(master, 0.0))

    def end(self, command_status):
        """
        Runs the catch ball command on the receiving robot if this command completed successfully
        :param command_status: The status of the command when its execution was ended
        """
        target_robot = self.team_bots.robots[self.target_robot_id]

        if target_robot is None:
            return

        # Run the catch ball command on the robot we're passing to
        from simclient.test.catch_ball import CatchBall
        target_robot.run_command(CatchBall(self.master))
        del CatchBall


CommandSeries.register(PassToRobot)
