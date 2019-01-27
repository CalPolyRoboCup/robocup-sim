from ..command import Command, CommandStatus


class TestCommand(Command):
    def assigned(self):
        print("Assigned!")

    def start(self):
        pass
        print("Start!")

    def update(self, delta_time: float):
        pass
        print("Update!")

    def get_status(self) -> CommandStatus:
        return CommandStatus.RUNNING

    def interrupted(self):
        pass
        print("Interrupted!")

    def end(self):
        pass
        print("End!")
