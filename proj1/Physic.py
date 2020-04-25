import math
import re
import numpy as np

class Point:

    x = 0
    y = 0


    def __init__(self, x):
        self.x = x
        self.y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y


    def toVector(self):
        return Vector(self.x, self.y)

    def __iadd(self, other):
        if isinstance(other, Point) or isinstance(other, Vector):
            return Point(self.x + other.x, self.y + other.y)
        else:
            return self

    def __str__(self):
        return "({:0.2f},{:0.2f})".format(self.x, self.y)

class Vector:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = math.atan2(y, x)


    def __add__(self, vector2):
        return Vector(self.x + vector2.x, self.y + vector2.y)

    def __str__(self):
        return "[{:0.2f},{:0.2f}]".format(self.x, self.y)

    def toPoint(self):
        return Point(self.x, self.y)


class Throw:

    replacements = {
        "sin": "np.sin",
        "cos": "np.cos",
        "exp": "np.exp",
        "sqrt": "np.sqrt",
        "^": "**"
    }

    def __init__(self,id , cannon_x, cannon_y, target_x, target_y, v_x, v_y, w_x, w_y, time_array, function):
        self.gravity = 9.81
        self.id = id
        self.cannon = Point(cannon_x, cannon_y)
        self.target = Point(target_x, target_y)
        self.initial_velocity = Vector(v_x, v_y)
        self.velocity = self.initial_velocity
        self.wind = Vector(w_x, w_y)
        self.times_array = time_array
        self.points_in_times = [Point(self.distance_x(time), self.distance_y(time)) for time in self.times_array]
        self.velocity_in_times = [Point(self.velocity_x(time), self.velocity_y(time)) for time in self.times_array]
        self.function = self.create_function(function)
        self.function_string = function
        self.end_time = None #modified in find_hitted_point()
        self.hitted_point = self.find_hitted_point()
        self.time_for_max_high = self.get_time_for_max_hight()
        self.max_hight = self.distance_y(self.time_for_max_high)

    def __init__(self, id, cannon, target, velocity, wind, time_array, function):
        self.gravity = 9.81
        self.id = id
        self.cannon = cannon
        self.target = target
        self.initial_velocity = velocity
        self.velocity = self.initial_velocity
        self.wind = wind
        self.times_array = time_array
        self.points_in_times = [Point(self.distance_x(time), self.distance_y(time)) for time in self.times_array]
        self.velocity_in_times = [Point(self.velocity_x(time), self.velocity_y(time)) for time in self.times_array]
        self.function = self.create_function(function)
        self.function_string = function
        self.end_time = None  # modified in find_hitted_point()
        self.hitted_point = self.find_hitted_point()
        self.time_for_max_high = self.get_time_for_max_hight()
        self.max_hight = self.distance_y(self.time_for_max_high)

    def __init__(self, id, initial_conditions):
        ic = initial_conditions
        self.gravity = 9.81
        self.id = id
        self.cannon = Point(ic[0], ic[1])
        self.target = Point(ic[2], ic[3])
        self.initial_velocity = Vector(ic[4], ic[5])
        self.velocity = self.initial_velocity
        self.wind = Vector(ic[6], ic[7])
        self.times_array = ic[8:-1]
        self.points_in_times = [Point(self.distance_x(time), self.distance_y(time)) for time in self.times_array]
        self.velocity_in_times = [Point(self.velocity_x(time), self.velocity_y(time)) for time in self.times_array]
        self.function = self.create_function(ic[-1])
        self.function_string = ic[-1]
        self.end_time = None  # modified in find_hitted_point()
        self.hitted_point = self.find_hitted_point()
        self.time_for_max_high = self.get_time_for_max_hight()
        self.max_hight = self.distance_y(self.time_for_max_high)

    def create_function(self, function_string):

        function_string = re.sub(r'([0-9.)]+)([([a-zA-Z]+)', r'\g<1>*\g<2>', function_string)


        for old, new in self.replacements.items():
            function_string = function_string.replace(old, new)

        def func(x):
            return eval(function_string)

        return func

    def distance_x(self, t):
        return distance(t, self.wind.x, self.initial_velocity.x, self.cannon.x)

    def distance_y(self, t):
        return distance(t, self.wind.y - self.gravity, self.initial_velocity.y, self.cannon.y)

    def velocity_x(self, t):
        return velocity(t, self.wind.x, self.initial_velocity.x)

    def velocity_y(self, t):
        return velocity(t, self.wind.y, self.initial_velocity.y)

    def has_hitted_map(self, t):
        position_x = self.distance_x(t)
        position_y = self.distance_y(t)

        diff = 0.005

        if -diff <= self.function(position_x) - position_y <= diff:
            return True
        else:
            return False

    def find_hitted_point(self, initial_time = 0, delta = 0.5):

        if self.has_hitted_map(initial_time) and initial_time > 0.0001:
            self.end_time = initial_time
            hitted_point = Point(self.distance_x(initial_time), self.distance_y(initial_time))
            self.has_hitted = touch(hitted_point, self.target)
            return hitted_point
        else:

            if self.distance_y(initial_time) >= self.function(self.distance_x(initial_time)):
                condition = lambda t: self.distance_y(t) >= self.function(self.distance_x(t))
            else:
                condition = lambda t: self.distance_y(t) < self.function(self.distance_x(t))

            time = initial_time + delta

            while(condition(time)):
                time += delta

            return self.find_hitted_point(time, -delta / 2)

    def get_time_for_max_hight(self):

        t_0 = 0
        t_max = self.end_time
        step = 0.1
        t_i = t_0 + step
        while(t_i < t_max and self.distance_y(t_i) < self.distance_y(t_i + step) ):
            t_i += step

        step = step / 100

        while(self.distance_y(t_i) < self.distance_y(t_i - step)):
            t_i -= step

        return t_i

    def __str__(self):
        throw_string = "Throw {}".format(self.id)
        throw_string += "  Cannon:   {}".format(self.cannon) + "\n"
        throw_string += "  Target:   {}".format(self.target) + "\n"
        throw_string += "  Hitted:   {}".format(self.hitted_point) + "\n"
        throw_string += "  Velocity: {}".format(self.initial_velocity) + "\n"
        throw_string += "  Wind:     {}".format(self.wind) + "\n"
        times_string =  "  Times:\n"
        for i in range(len(self.times_array)):
            times_string += "  --time_{}:  {}\n".format(i+1, self.times_array[i])
        throw_string += times_string + "\n"
        throw_string += self.function_string + "\n"
        return throw_string

def distance(t, a = 0, v_0 = 0, s_0 = 0):
    return s_0 + v_0*t + 0.5*(a*t**2)

def velocity(t, a, v_0):
    return v_0 + a*t

def touch(point1, point2):
    x_range = point2.x - point1.x
    y_range = point2.y - point1.y
    return x_range**2 + y_range**2 < 0.05**2

