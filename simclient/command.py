from abc import *
from enum import Enum


class CommandStatus(Enum):
    """
    An enumeration used to indicate the status of a command
    """
    RUNNING = 0
    COMPLETED = 1
    FAILED = 2


class Command(ABC):
    """
    Used to define a core skill or behavior of a robot
    """
    def __init__(self, master):
        """
        Initializes a new Command
        """
        self.team_bots = master.team_bots
        self.other_bots = master.other_bots
        self.field = master.field
        self.ball = master.ball
        self.master = master

        self._robot = None

    def set_robot(self, robot) -> bool:
        """
        Sets the parent robot to the given robot, if possible
        :param robot: The robot to assign this command to
        :return: True if the command could be assigned to the given robot, otherwise False
        """
        if self._robot is not None:
            return False

        self._robot = robot
        self.assigned()

        return True

    def get_robot(self):
        """
        Returns the robot assigned with this command
        :return: The robot assigned with this command
        """
        return self._robot

    def is_finished(self) -> bool:
        """
        Returns true if the command has finished execution
        :return: True if the command has finished execution, otherwise False
        """
        return self.get_status() != CommandStatus.RUNNING

    @abstractmethod
    def assigned(self):
        """
        Called when the command is first assigned to a robot
        """
        pass

    @abstractmethod
    def start(self):
        """
        Called when the command starts execution
        """
        pass

    @abstractmethod
    def update(self, delta_time: float):
        """
        Called continuously throughout the command's execution
        :param delta_time: The time passed since the last update
        """
        pass

    @abstractmethod
    def get_status(self) -> CommandStatus:
        """
        Used to determine if this command has finished executing
        :return: True if the command has finished executing, otherwise False
        """
        return CommandStatus.RUNNING

    @abstractmethod
    def interrupted(self):
        """
        Called when this command is interrupted by another command
        """
        pass

    @abstractmethod
    def end(self, command_status: CommandStatus):
        """
        Called when this command quits execution
        :param command_status: The status of the command when its execution was ended
        """
        pass
