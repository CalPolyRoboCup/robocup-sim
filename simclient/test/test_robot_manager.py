from ..robot_manager import RobotManager
from ..robot import Robot
from .test_command import TestCommand


class TestRobotManager(RobotManager):
    def init_robot(self, robot: Robot):
        pass
        # if robot.id == 0:
        #     robot.set_default_command(TestCommand())

    def update(self, delta_time):
        pass
