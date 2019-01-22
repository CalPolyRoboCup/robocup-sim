from simclient.client import Client

from simclient.team import Team


def run():
    """
    Starts and runs the client
    """
    client = Client("SimClient", 1280, 720, Team.YELLOW)
    client.run()


if __name__ == "__main__":
    run()
