from proto.messages_robocup_ssl_wrapper_pb2 import SSL_WrapperPacket

from simclient.master import Master

from proto.grSim_Packet_pb2 import grSim_Packet

from simclient.team import Team
from simclient.robot import Robot
from simclient.communication.sim_receiver import SimReceiver
from simclient.communication.sim_sender import SimSender

from simclient.commands.aim_at_robot import AimAtRobot


class Client(Master):
    """
    The class that manages graphics, input, running AI logic, and communicating with grSim
    """
    def __init__(self, title: str, width: int, height: int, team: Team):
        """
        Initializes a new Client instance
        :param title: The title of the window
        :param width: The width of the window
        :param height: The height of the window
        :param team: The team the client is controlling
        """
        super().__init__(title, width, height, team)
        self.receiver = SimReceiver()
        self.receiver.open()
        self.sender = SimSender()
        self.sender.connect()

    def update_ai(self, delta_time: float):
        """
        Updates AI logic
        :param delta_time: The time passed since the last update
        """
        pass

    def receive_packet(self) -> SSL_WrapperPacket:
        """
        Receives and returns a packet from grSim
        :return: A new packet from grSim
        """
        return self.receiver.receive()

    def send_commands(self):
        """
        Sends all robot outputs in a packet to grSim
        """
        sim_packet = grSim_Packet()
        sim_packet.commands.isteamyellow = self.team_bots.team == Team.YELLOW
        sim_packet.commands.timestamp = 0

        self.team_bots.write_output(sim_packet.commands.robot_commands)
        self.sender.send(sim_packet)

    def init_team_robot(self, robot: Robot):
        """
        Initializes a new team robot when initially detected
        :param robot: The new robot
        """
        if robot.id == 0:
            robot.run_command(AimAtRobot(self, 1))
        pass

    def init_other_robot(self, robot: Robot):
        """
        Initializes a new opponent robot when initially detected
        :param robot: The new robot
        """
        pass
