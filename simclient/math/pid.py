class PID:
    def __init__(self, p: float, i: float, d: float, min_out: float, max_out: float):
        """
        Initializes a new PID instance
        :param p: The potential parameter
        :param i: The integral parameter
        :param d: The derivative parameter
        :param min_out: The minimum output value
        :param max_out: The maximum output value
        """
        self.p = p
        self.i = i
        self.d = d
        self.min_out = min_out
        self.max_out = max_out
        self.set_point = 0
        self._last_error = 0
        self._integral = 0

    def calculate(self, delta_time: float, input_val: float) -> float:
        """
        Runs a PID iteration
        :param delta_time: The time passed since the last iteration
        :param input_val: The input to the PID calculation
        :return: The output of the current iteration
        """

        # Calculate the error and P values
        error = self.set_point - input_val
        p_out = self.p * error

        # Calculate the I value
        self._integral += error * delta_time
        i_out = self.i * self._integral

        # Calculate the D value
        derivative = (error - self._last_error) / delta_time
        d_out = self.d * derivative

        # Calculate the output
        output = p_out + i_out + d_out

        # Min-max the output
        if output > self.max_out:
            output = self.max_out
        elif output < self.min_out:
            output = self.min_out

        # Cache the last error
        self._last_error = error

        return output
