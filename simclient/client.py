import sys

import pygame

from simclient.comms.sim_receiver import SimReceiver
from simclient.comms.sim_sender import SimSender
from simclient.robot_manager import RobotManager
from simclient.ball import Ball
from simclient.field import Field
from simclient.team import Team

from proto.grSim_Packet_pb2 import grSim_Packet


class Client:
    """
    The class that manages graphics, input, and updating the simulation
    """
    BACKGROUND_COLOR = (0, 95, 0)
    DEFAULT_SCALE = 0.1
    MAX_SCALE = 1.0
    MIN_SCALE = 0.05
    SCALE_RATE = 1.05

    def __init__(self, title: str, width: int, height: int, team: Team):
        """
        Initializes a new Client instance
        :param title: The title of the window
        :param width: The width of the window
        :param height: The height of the window
        :param team: The team that the code is controlling
        """
        self.width = width
        self.height = height
        self.team = team
        self.scale = Client.DEFAULT_SCALE
        self.receiver = SimReceiver()
        self.receiver.open()
        self.sender = SimSender()
        self.sender.connect()
        self.yellow_bots = RobotManager(Team.YELLOW)
        self.blue_bots = RobotManager(Team.BLUE)
        self.ball = Ball()
        self.field = Field()
        self.team_bots = self.yellow_bots if team == Team.YELLOW else self.blue_bots
        self.last_frame_number = None
        self.last_frame_time = None

        # Initialize pygame and set the proper window properties
        pygame.init()
        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode((self.width, self.height))

    def run(self):
        """
        Updates the simulation, renders, and handles inputs
        """
        # Main event/update loop
        while True:
            # Poll window events and handle input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.scale *= Client.SCALE_RATE
                    elif event.button == 5:
                        self.scale /= Client.SCALE_RATE

                    self.scale = min(Client.MAX_SCALE, max(Client.MIN_SCALE, self.scale))

            # Receive the latest packet from grSim
            wrapper_packet = self.receiver.receive()

            if wrapper_packet is None:
                continue

            frame = wrapper_packet.detection

            frame_number = frame.frame_number
            frame_time = frame.t_capture

            if self.last_frame_number is None:
                # If we don't know how much time has passed since the last update, record this instance as the last time
                self.last_frame_number = frame_number
                self.last_frame_time = frame_time
            else:
                # Find out how many frames have passed since the last update
                delta_frames = frame_number - self.last_frame_number

                if delta_frames > 0:
                    # If more than 1 frame has passed, the packet has changed, so let's update and render the simulation
                    self.update(frame_time - self.last_frame_time)
                    self.send_commands()
                    self.render()

                    self.last_frame_number = frame_number
                    self.last_frame_time = frame_time

            # Decode robot information form the packet
            self.yellow_bots.decode(frame.robots_yellow)
            self.blue_bots.decode(frame.robots_blue)

            # Find the first valid ball in the frame (this works great for grSim, might want to change for SSL_Vision)
            frame_ball = next((item for item in frame.balls if item is not None), None)

            if frame_ball is not None:
                self.ball.decode(frame_ball)

            # Decode field geometry information
            self.field.decode(wrapper_packet.geometry.field)

    def update(self, delta_time: float):
        """
        Update outgoing packet information for the controlled team
        :param delta_time: The amount of time passed since the last  update
        """
        self.yellow_bots.update_stats(delta_time)
        self.blue_bots.update_stats(delta_time)
        self.ball.update_stats(delta_time)
        self.team_bots.update_commands(delta_time)

    def send_commands(self):
        """
        Sends all robot outputs in a packet to grSim
        """
        sim_packet = grSim_Packet()
        sim_packet.commands.isteamyellow = self.team == Team.YELLOW
        sim_packet.commands.timestamp = 0

        self.team_bots.write_output(sim_packet.commands.robot_commands)
        self.sender.send(sim_packet)

    def render(self):
        """
        Renders everything to the screen
        """
        self.screen.fill(Client.BACKGROUND_COLOR)

        self.field.render(self)
        self.yellow_bots.render(self)
        self.blue_bots.render(self)
        self.ball.render(self)

        pygame.display.flip()

    def screen_point(self, x: float, y: float) -> (int, int):
        """
        Converts real-life coordinates to screen coordinates
        :param x: The x-coordinate
        :param y: The y-coordinate
        :return: A tuple containing the screen coordinates
        """
        return int(round(x * self.scale + self.width * 0.5)), int(round(-y * self.scale + self.height * 0.5))

    def screen_scalar(self, value: float) -> int:
        """
        Converts a real-life scalar to a screen scalar
        :param value: The value to scale
        :return: The scaled value
        """
        return int(round(value * self.scale))
