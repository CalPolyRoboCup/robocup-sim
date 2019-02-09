import logging

from abc import abstractmethod

from .command import Command, CommandStatus


class FailResponse:
    """
    Used for defining how a command series should respond to a child command's failure
    """
    CONTINUE = 0
    RETRY = 1
    FAIL = 2


class CommandSeries(Command):
    """
    Used for chaining a series of commands together and defining what happens between commands in the chain
    """
    def __init__(self, master):
        """
        Initializes a new CommandSeries
        :param master: The master instance
        """
        super(CommandSeries, self).__init__(master)
        self.logger = logging.getLogger(__name__)
        self.command = None
        self.fail_response = None
        self.commands = []
        self.status = CommandStatus.RUNNING
        self.index = 0

    def add_command(self, command, fail_response=FailResponse.CONTINUE):
        """
        Adds a command to the command series, with an optional fail response
        :param command: The command to be executed
        :param fail_response: Indicates what should happen if the provided command fails in execution
        """
        self.commands.append((command, fail_response))

    def assigned(self):
        """
        Assigns all commands in the series to the robot assigned to this command series
        :return:
        """
        for command in self.commands:
            if not command[0].set_robot(self.get_robot()):
                self.logger.log(logging.WARNING, "Cannot add commands to a command series that have already been added"
                                                 "to another robot!")

    def start(self):
        """
        Starts the command series
        """
        self.index = 0
        self.status = CommandStatus.RUNNING

        if len(self.commands) > 0:
            (self.command, self.fail_response) = self.commands[0]
            self.command.start()
        else:
            self.command = None
            self.status = CommandStatus.COMPLETED

    def update(self, delta_time):
        """
        Updates the command series
        :param delta_time: The time passed since the last update
        """
        command_status = self.command.get_status()

        if command_status == CommandStatus.COMPLETED:
            # If the command has completed successfully, try to start the next command in the series
            if not self._start_next(command_status):
                # If there are no more commands in the series, indicate that the command series has completed
                self.status = CommandStatus.COMPLETED
                return
        elif command_status == CommandStatus.FAILED:
            # If the command failed in some way, handle the failure according to the indicated failure response
            if self.fail_response == FailResponse.CONTINUE:
                # If we are supposed to continue anyway, try to start the next command in the series
                if not self._start_next(command_status):
                    # If there are no more commands in the series, indicate that the command series has completed
                    self.status = CommandStatus.COMPLETED
                    return
            elif self.fail_response == FailResponse.RETRY:
                # If we are supposed to retry the command, do so
                self.command.end(command_status)
                self.command.start()
            elif self.fail_response == FailResponse.FAIL:
                # If we are supposed to fail if this command fails, then indicate that the command series has failed
                self.status = CommandStatus.FAILED
                return

        # Update the active command
        self.command.update(delta_time)

    def get_status(self):
        """
        Returns the current status of the command series
        :return: The current status of the command series
        """
        return self.status

    @abstractmethod
    def end(self, command_status):
        """
        Called when this command ends execution
        :param command_status: The status of the command when its execution was ended
        """
        pass

    def _start_next(self, command_status):
        """
        Attempts to start the next command in the series
        :return: True if the next command was started, False if there are no more commands in the series to start
        """
        self.command.end(command_status)

        if self.index < len(self.commands) - 1:
            self.index += 1
            (self.command, self.fail_response) = self.commands[self.index]
            self.command.start()
            return True
        else:
            self.status = CommandStatus.COMPLETED
            return False


Command.register(CommandSeries)