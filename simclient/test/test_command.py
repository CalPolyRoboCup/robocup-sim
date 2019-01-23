from ..command import Command


class TestCommand(Command):
    def assigned(self):
        pass
        # print("Assigned!")

    def start(self):
        pass
        # print("Start!")

    def update(self, delta_time: float):
        pass
        # print("Update!")

    def is_finished(self) -> bool:
        return False

    def interrupted(self):
        pass
        # print("Interrupted!")

    def end(self):
        pass
        # print("End!")
