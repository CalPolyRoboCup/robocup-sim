import math

from .vector2 import Vector2


class MathHelper:
    """
    Contains helper for complex mathematical procedures
    """
    @staticmethod
    def adjust_angle_value(base_angle: float, other_angle: float) -> float:
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

    @staticmethod
    def get_line_angle(point_a: Vector2, point_b: Vector2) -> float:
        """
        Returns the angle in radians of the line drawn from point A to point B
        :param point_a: The first point in the line
        :param point_b: The second point in the line
        :return: A float representing the radians of the line drawn from point A to point B
        """
        return math.atan2(point_b.y - point_a.y, point_b.x - point_a.x)

    @staticmethod
    def get_closest_point(line_start: Vector2, line_end: Vector2, point: Vector2):
        """
        Returns the point along the given line closest to the point provided
        :param line_start: The start of the line
        :param line_end: The end of the line
        :param point: The point to compare with the line
        :return: A Vector2 describing the point along the line closest to the point provided
        """
        direction = (line_end - line_start).normalized()

        t = direction.x * (point.x - line_start.x) + direction.y * (point.y - line_start.y)

        return Vector2(t * direction.x + line_start.x, t * direction.y + line_start.y)
