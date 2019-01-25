from simclient.client import Client

from simclient.team import Team


def run():
    """
    Starts and runs the client
    """
    master = Client("Cal Poly RoboCup", 1280, 720, Team.YELLOW)
    master.run()


if __name__ == "__main__":
    run()
