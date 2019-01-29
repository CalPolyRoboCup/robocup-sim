from simclient.command import Command, CommandStatus


class Delay(Command):
    """
    Waits for the given amount of time before proceeding to the next command
    """
    def __init__(self, master, seconds: float):
        """
        Initializes a new Delay instance
        :param master: The Master instance
        :param seconds: The number of seconds to delay
        """
        super().__init__(master)
        self.delay_time = seconds
        self.seconds_passed = 0.0

    def assigned(self):
        """
        Not implemented
        """
        pass

    def start(self):
        """
        Resets the delay timer
        """
        self.seconds_passed = 0.0

    def update(self, delta_time: float):
        """
        Updates the timer
        :param delta_time: The time passed since the last update
        """
        self.seconds_passed += delta_time

    def get_status(self) -> CommandStatus:
        """
        Returns the status of this command
        :return: The status of this command
        """
        return CommandStatus.COMPLETED if self.seconds_passed >= self.delay_time else CommandStatus.RUNNING

    def interrupted(self):
        """
        Not implemented
        """
        pass

    def end(self, command_status: CommandStatus):
        """
        Not implemented
        """
        pass
