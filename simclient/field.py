import pygame

from proto.messages_robocup_ssl_geometry_pb2 import SSL_GeometryFieldSize


class Field:
    """
    Decodes and renders geometry packets from grSim
    """
    LINE_COLOR = (255, 255, 255)
    LINE_THICKNESS = 20

    def __init__(self):
        """
        Initializes the Field instance
        """
        self.last_packet = None
        self.field_length = 0
        self.field_width = 0
        self.goal_width = 0
        self.goal_depth = 0
        self.boundary_width = 0
        self.field_lines = []
        self.field_arcs = []

    def decode(self, field_size: SSL_GeometryFieldSize):
        """
        Decodes the SSL_GeometryFieldSize packet, scaling the geometry to match the scale of the client
        :param field_size: The SSL_GeometryFieldSize packet to decode
        :return:
        """
        if field_size.field_width == 0:
            return
            # If any of the packet's fields were 0, geometry data most likely wasn't updated, so we don't update

        for key in self.__dict__.keys():
            # Find all the fields in this instance that have matching names in the packet object, and update accordingly
            try:
                attr = getattr(field_size, key)
            except AttributeError:
                continue

            setattr(self, key, attr)

    def render(self, client):
        """
        Renders the field geometry to the screen
        :param client: The client which to render the geometry
        """
        # Draw the rectangle outline
        pygame.draw.rect(client.screen, Field.LINE_COLOR, pygame.Rect(
             client.width * 0.5 - client.screen_scalar(self.field_length) * 0.5,
             client.height * 0.5 - client.screen_scalar(self.field_width) * 0.5,
             client.screen_scalar(self.field_length), client.screen_scalar(self.field_width)
        ), client.screen_scalar(Field.LINE_THICKNESS))

        # Draw the left goal
        pygame.draw.rect(client.screen, Field.LINE_COLOR, pygame.Rect(
            client.width * 0.5 - client.screen_scalar(self.field_length) * 0.5 -
            client.screen_scalar(self.goal_depth),
            client.height * 0.5 - client.screen_scalar(self.goal_width) * 0.5,
            client.screen_scalar(self.goal_depth), client.screen_scalar(self.goal_width)
        ), client.screen_scalar(Field.LINE_THICKNESS))

        # Draw the right goal
        pygame.draw.rect(client.screen, Field.LINE_COLOR, pygame.Rect(
            client.width * 0.5 + client.screen_scalar(self.field_length) * 0.5,
            client.height * 0.5 - client.screen_scalar(self.goal_width) * 0.5,
            client.screen_scalar(self.goal_depth), client.screen_scalar(self.goal_width)
        ), client.screen_scalar(Field.LINE_THICKNESS))
