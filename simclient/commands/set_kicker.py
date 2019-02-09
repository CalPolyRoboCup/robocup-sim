from simclient.command import Command, CommandStatus


class SetKicker(Command):
    """
    Sets the speed of the kicker
    """
    def __init__(self, master, speed):
        """
        Initializes a new SetKicker instance
        :param master: The Master instance
        :param speed: The speed to set the kicker
        """
        super(SetKicker, self).__init__(master)
        self.speed = speed

    def assigned(self):
        """
        Not implemented
        """
        pass

    def start(self):
        """
        Sets the kicker speed to the indicated value
        """
        self.get_robot().set_kicker_speed(self.speed)

    def update(self, delta_time):
        """
        Not implemented
        """
        pass

    def get_status(self):
        """
        Returns the status of the command
        :return: COMPLETED
        """
        return CommandStatus.COMPLETED

    def end(self, command_status):
        """
        Not implemented
        """
        pass
