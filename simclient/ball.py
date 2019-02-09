import math

import pygame

from simclient.util.vector2 import Vector2

from proto.messages_robocup_ssl_detection_pb2 import SSL_DetectionBall


class Ball:
    """
    Decodes and renders ball packets from grSim
    """
    COLOR = (255, 127, 0)
    RADIUS = 22
    OUTLINE_SIZE = 1

    def __init__(self):
        """
        Initializes a new Ball instance
        """
        self.position = Vector2()
        self.last_position = None
        self.speed = 0
        self.direction = 0

    def decode(self, det_ball):
        """
        Decodes the given SSL_DetectionBall packet
        :param det_ball: The SSL_DetectionBall packet to decode
        """
        # Update the position information
        self.position.set(det_ball.x, det_ball.y)

        # Update the last position information if it hasn't been set yet
        if self.last_position is None:
            self.last_position = self.position.copy()

    def update_stats(self, delta_time):
        """
        Updates the velocity stats for the ball
        :param delta_time: The time passed since the last update
        """
        if self.last_position is None or self.position == self.last_position:
            return

        # If the ball has moved since the last update, update its speed information
        self.speed = (self.position - self.last_position).length() / delta_time * 0.001

        if self.speed > 0:
            self.direction = math.atan2(-(self.position.y - self.last_position.y),
                                        self.position.x - self.last_position.x)

        self.last_position.copy_from(self.position)

    def render(self, client):
        """
        Renders the ball to the given client
        :param client: The client which to render the ball
        """
        # Draw the filled circle for the ball
        pygame.draw.circle(client.screen, Ball.COLOR,
                           client.screen_point(self.position.x, self.position.y),
                           client.screen_scalar(Ball.RADIUS))

        # Draw the ball's outline
        pygame.draw.circle(client.screen, (0, 0, 0),
                           client.screen_point(self.position.x, self.position.y),
                           client.screen_scalar(Ball.RADIUS) + Ball.OUTLINE_SIZE, Ball.OUTLINE_SIZE)
