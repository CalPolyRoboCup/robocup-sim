from abc import *


class Command(ABC):
    """
    Used to define a core skill or behavior of a robot
    """
    def __init__(self):
        """
        Initializes a new Command
        """
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
    def is_finished(self) -> bool:
        """
        Used to determine if this command has finished executing
        :return: True if the command has finished executing, otherwise False
        """
        return False

    @abstractmethod
    def interrupted(self):
        """
        Called when this command is interrupted by another command
        """
        pass

    @abstractmethod
    def end(self):
        """
        Called when this command quits execution
        """
        pass
