import pygame

from ..command import Command, CommandStatus
from ..math.vector2 import Vector2
from ..math.math_helper import MathHelper


class MoveToMouse(Command):
    """
    Makes the robot follow the mouse
    """
    def assigned(self):
        """
        Not implemented
        """
        pass

    def start(self):
        """
        Not implemented
        """
        pass

    def update(self, delta_time: float):
        """
        Updates the robot's motor outputs to move toward the mouse
        :param delta_time: The time since the last update
        """
        # Get robot running the command
        robot = self.get_robot()

        # Get mouse position vector
        mouse_pos = pygame.mouse.get_pos()
        mouse_vec = Vector2(mouse_pos[0], mouse_pos[1])

        # Set angle and orientation toward mouse
        angle = MathHelper.get_line_angle(robot.screen_pos, mouse_vec)
        robot.set_target_direction(angle)
        robot.set_target_orientation(-angle)

        # Move toward mouse if mouse is pressed
        robot.set_target_speed(1.0 if pygame.mouse.get_pressed()[0] else 0.0)

        # Activate the kicker if the right mouse button is pressed
        robot.set_kicker_speed(3.0 if pygame.mouse.get_pressed()[2] else 0.0)

    def get_status(self) -> CommandStatus:
        """
        Return CommandStatus.RUNNING, since this command never terminates
        """
        return CommandStatus.RUNNING

    def end(self, command_status: CommandStatus):
        """
        Not implemented
        """
        pass
