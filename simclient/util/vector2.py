import math


class Vector2:
    """
    Represents a vector in 2D coordinates
    """
    def __init__(self, x: float = 0.0, y: float = 0.0):
        """
        Initializes this instance from the given x and y coordinates
        :param x: The x-coordinate
        :param y: the y-coordinate
        """
        self.x = x
        self.y = y

    def set(self, x: float, y: float):
        """
        Sets the x and y coordinates of this instance from the given x and y coordinates
        :param x: The x-coordinate
        :param y: The y-coordinate
        """
        self.x = x
        self.y = y

    def copy(self) -> 'Vector2':
        """
        Returns a copy of this Vector2
        :return: A copy of this Vector2
        """
        return Vector2(self.x, self.y)

    def copy_from(self, other: 'Vector2'):
        """
        Copies the x and y coordinates from another Vector2 into this instance
        :param other: The other Vector2
        """
        self.x = other.x
        self.y = other.y

    def length(self) -> float:
        """
        Calculates the length of this Vector2
        :return: The length of this Vector2
        """
        return math.sqrt(self.x * self.x + self.y * self.y)

    def normalized(self) -> 'Vector2':
        """
        Calculates and returns a normalized copy of this vector
        :return: A normalized copy of this vector
        """
        length = self.length()
        return Vector2(self.x / length, self.y / length)

    def __add__(self, other: 'Vector2') -> 'Vector2':
        """
        Adds another Vector2 to this one
        :param other: The other Vector2
        """
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vector2') -> 'Vector2':
        """
        Subtracts another Vector2 from this one
        :param other: The other Vector2
        """
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> 'Vector2':
        """
        Calculates and returns a scaled copy of this vector
        :param scalar: The factor by which to scale this vector
        :return: The scaled copy of this vector
        """
        return Vector2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float) -> 'Vector2':
        """
        Calculates and returns a scaled copy of this vector
        :param scalar: The factor by which to scale this vector
        :return: The scaled copy of this vector
        """
        return Vector2(self.x / scalar, self.y / scalar)

    def __len__(self):
        """
        Calculates the length of this Vector2
        :return: The length of this Vector2
        """
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __str__(self):
        """
        Converts this vector2 to a string
        :return: This vector2 represented as a string
        """
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __eq__(self, other):
        """
        Checks if this Vector2 is equal to another Vector2
        :param other: The other Vector2
        :return: True if the vectors are equal, otherwise False
        """
        return other is Vector2 and self.x == other.x and self.y == other.y
