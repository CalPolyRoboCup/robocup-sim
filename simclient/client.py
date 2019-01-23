from proto.messages_robocup_ssl_wrapper_pb2 import SSL_WrapperPacket

from simclient.master import Master

from proto.grSim_Packet_pb2 import grSim_Packet

from .robot_manager import RobotManager

from .team import Team

from .communication.sim_receiver import SimReceiver
from .communication.sim_sender import SimSender


class Client(Master):
    """
    The class that manages graphics, input, running AI logic, and communicating with grSim
    """
    def __init__(self, title: str, width: int, height: int, robot_manager: RobotManager):
        """
        Initializes a new Client instance
        :param title: The title of the window
        :param width: The width of the window
        :param height: The height of the window
        :param robot_manager: The robot manager to control our team
        """
        super().__init__(title, width, height, robot_manager)
        self.receiver = SimReceiver()
        self.receiver.open()
        self.sender = SimSender()
        self.sender.connect()

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