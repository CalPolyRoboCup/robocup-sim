import math


class MathHelper:
    """
    Contains helper for complex mathematical procedures
    """
    @staticmethod
    def adjust_angle_value(base_angle: float, other_angle: float):
        """
        Adjusts an angle so that two angles are within 2 * pi distance of each other
        :param base_angle: The angle to remain constant
        :param other_angle: The angle to be adjusted
        :return: The adjusted angle
        """
        while base_angle - other_angle > math.pi:
            other_angle += math.pi * 2

        while other_angle - base_angle > math.pi:
            other_angle -= math.pi * 2

        return other_angle
