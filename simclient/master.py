import sys

import pygame

from abc import ABCMeta, abstractmethod

from simclient.robot_manager import RobotManager
from simclient.ball import Ball
from simclient.field import Field
from simclient.team import Team
from simclient.robot import Robot

from proto.messages_robocup_ssl_wrapper_pb2 import SSL_WrapperPacket


class Master(object):
    __metaclass__ = ABCMeta

    """
    The class that manages graphics, input, and running AI logic
    """
    BACKGROUND_COLOR = (0, 95, 0)
    DEFAULT_SCALE = 0.1
    MAX_SCALE = 1.0
    MIN_SCALE = 0.05
    SCALE_RATE = 1.05

    def __init__(self, title, width, height, team):
        """
        Initializes a new Master instance
        :param title: The title of the window
        :param width: The width of the window
        :param height: The height of the window
        :param team: The team the client is controlling
        """
        self.width = width
        self.height = height
        self.scale = Master.DEFAULT_SCALE
        self.ball = Ball()
        self.field = Field()
        self.last_frame_number = None
        self.last_frame_time = None
        self.yellow_bots = RobotManager(Team.YELLOW)
        self.blue_bots = RobotManager(Team.BLUE)

        if team == Team.YELLOW:
            self.team_bots = self.yellow_bots
            self.other_bots = self.blue_bots
        else:
            self.team_bots = self.blue_bots
            self.other_bots = self.yellow_bots

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
                        self.scale *= Master.SCALE_RATE
                    elif event.button == 5:
                        self.scale /= Master.SCALE_RATE

                    self.scale = min(Master.MAX_SCALE, max(Master.MIN_SCALE, self.scale))

            # Receive the latest packet
            wrapper_packet = self.receive_packet()

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
            self.team_bots.decode(frame.robots_yellow, self.init_team_robot)
            self.blue_bots.decode(frame.robots_blue, self.init_other_robot)

            # Find the first valid ball in the frame (this works great for grSim, might want to change for SSL_Vision)
            frame_ball = next((item for item in frame.balls if item is not None), None)

            if frame_ball is not None:
                self.ball.decode(frame_ball)

            # Decode field geometry information
            self.field.decode(wrapper_packet.geometry.field)

    def update(self, delta_time):
        """
        Update outgoing packet information for the controlled team
        :param delta_time: The amount of time passed since the last  update
        """
        # Update stats the robots and ball
        self.yellow_bots.update_stats(delta_time)
        self.blue_bots.update_stats(delta_time)
        self.ball.update_stats(delta_time)

        # Update AI
        self.update_ai(delta_time)

        # Update commands
        self.team_bots.update_commands(delta_time)

    def render(self):
        """
        Renders everything to the screen
        """
        self.screen.fill(Master.BACKGROUND_COLOR)

        self.field.render(self)
        self.yellow_bots.render(self)
        self.blue_bots.render(self)
        self.ball.render(self)

        pygame.display.flip()

    def screen_point(self, x, y):
        """
        Converts real-life coordinates to screen coordinates
        :param x: The x-coordinate
        :param y: The y-coordinate
        :return: A tuple containing the screen coordinates
        """
        return int(round(x * self.scale + self.width * 0.5)), int(round(-y * self.scale + self.height * 0.5))

    def screen_scalar(self, value):
        """
        Converts a real-life scalar to a screen scalar
        :param value: The value to scale
        :return: The scaled value
        """
        return int(round(value * self.scale))

    @abstractmethod
    def update_ai(self, delta_time):
        """
        Used to update AI logic
        """
        pass

    @abstractmethod
    def init_team_robot(self, robot):
        """
        Called when SSL_Vision detects a new team robot on the field
        """
        pass

    @abstractmethod
    def init_other_robot(self, robot):
        """
        Called when SSL_Vision detects a new opponent robot on the field
        """
        pass

    @abstractmethod
    def receive_packet(self):
        """
        Used to receive packets from the vision system
        :return: A new vision packet
        """
        pass

    @abstractmethod
    def send_commands(self):
        """
        Used to send commands to the robots
        """
        pass
