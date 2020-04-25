import copy
import random

class Body:

    def __init__(self, id, x, y, vx, vy, m, color):
        self.id = id

        self.color = color

        self.history = []

        self.radius = 1
        self.mass = m

        self.point = Point(x, y)
        self.velocity = Point(vx, vy)

        self.collision_points = []

    def get_color(self):
        return self.color

    def add_pos(self, point):
        self.history.append(copy.deepcopy(point))

    def get_history(self):
        return self.history


    def get_id(self):
        return self.id

    def get_r(self):
        return self.radius

    def get_m(self):
        return self.mass

    def get_point(self):
        return self.point

    def set_point(self, point):
        self.point = point

    def get_velocity(self):
        return self.velocity

    def set_velocity(self, vel):
        self.velocity = vel


    def append_collision(self):
        self.collision_points.append([copy.deepcopy(self.point), copy.deepcopy(self.velocity)])

    def __add__(self, other):
        if type(other) == type(self):
            new_body = copy.deepcopy(self)
            new_body.point = (self.point + other.get_point())*0.5
            new_body.mass = self.mass + other.get_m()
            new_body.velocity = (self.velocity*self.mass+ other.get_velocity()*other.get_m()) * (1/self.mass)

            new_color = []
            for i in range(len(self.color)):
                new_color.append(random.random())

            new_body.color = new_color

            new_body.history = [copy.deepcopy(new_body.get_point())]

            return new_body
        else:
            raise Exception("Adding cannot be performed on {}".format(str(type(other))))

    def __and__(self, other):
        if type(other) == type(self):
            sq_r = (self.get_r() + other.get_r())**2
            sq_x = (self.get_point().get_x() - other.get_point().get_x())**2
            sq_y = (self.get_point().get_y() - other.get_point().get_y())**2
            return sq_r > sq_x + sq_y
        else:
            return False

    def __eq__(self, other):
        if type(other) == type(self):
            return self.point == other.get_point()
        else:
            return False

    def __str__(self):
        string = "  Ciało_{}:\n     m = {}\n     x = ({})\n     V = [{}]".format(self.id, self.mass, self.point, self.velocity)
        return string

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
         return self.y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def get_length(self):
        return (self.x**2 + self.y**2)**0.5

    def __add__(self, point):
        new_x = self.get_x() + point.get_x()
        new_y = self.get_y() + point.get_y()
        return Point(new_x, new_y)

    def __sub__(self, point):
        new_x = self.get_x() - point.get_x()
        new_y = self.get_y() - point.get_y()
        return Point(new_x, new_y)

    def __rmul__(self, other):
        return self*other

    def __mul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Point(self.get_x() * other, self.get_y() * other)
        elif(isinstance(other, Point)):
            return self.x*other.x + self.y*other.y

    def __pow__(self, other):
            return (self.x * other.y - self.y * other.x)  # croos pr`oduct length(negative or positive)

    def __truediv__(self, number):
        new_x = self.get_x()/number
        new_y = self.get_y()/number
        return Point(new_x, new_y)

    def __eq__(self, other):
        if type(other) == type(self):
            return self.x == other.get_x() and self.y == other.get_y
        else:
            return False

    def __abs__(self):
        return self.get_length()

    def __str__(self):
        return "{:.2f}, {:.2f}".format(self.x, self.y)