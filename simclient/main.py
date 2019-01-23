from simclient.client import Client

from simclient.team import Team

from simclient.test.test_robot_manager import TestRobotManager


def run():
    """
    Starts and runs the client
    """
    master = Client("Cal Poly RoboCup", 1280, 720, TestRobotManager(Team.YELLOW))
    master.run()

    # TODO: Make it easy to access robots by their id


if __name__ == "__main__":
    run()
