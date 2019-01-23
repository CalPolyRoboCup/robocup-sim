from ..command import Command
from ..robot import Robot
from ..util.vector2 import Vector2


class AimAtRobot(Command):
    def __init__(self, target_robot: Robot):
        super().__init__()
        self.target_robot = target_robot
        self.target_pos = Vector2()

    def assigned(self):
        pass

    def start(self):
        self.target_pos.set(0, 0)

    def update(self, delta_time: float):
        # TODO
        pass

    def is_finished(self) -> bool:
        pass

    def interrupted(self):
        pass

    def end(self):
        pass
