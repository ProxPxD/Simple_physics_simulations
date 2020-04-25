import copy

class Ball:

    def __init__(self, id, x, y, vx = 0, vy = 0, r=3*10**(-2)):
        self.radius = r
        self.mass = 17 * 10**(-3)

        self.id = id

        self.point = Point(x, y)
        self.velocity = Point(vx, vy)

        self.fall_out = False

        self.collsion_points = []
        self.colided = []

        self.counter = 0

    def check_if_fall_out(self):
        return self.fall_out

    def set_fall_out(self):
        self.fall_out = True

    def get_counter(self):
        return self.counter

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

    def set_point(self, x, y):
        self.point.set_x(x)
        self.point.set_y(y)

    def get_velocity(self):
        return self.velocity

    def set_velocity(self, vx, vy):
        self.velocity.set_x(vx)
        self.velocity.set_y(vy)

    def check_distance(self):
        for ball in self.colided:
            if (ball.get_point() - self.get_point()).get_length() > 1 and len(self.colided) > 0:
                self.colided.remove(ball)

    def append_collision(self, ball = None):
        if ball is not None:
            self.colided.append(ball)
            self.counter += 1
            #print(ball.get_point())
            #print(self.get_point())
            #print()
        self.collsion_points.append([copy.deepcopy(self.point), copy.deepcopy(self.velocity)])

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
        string = "  Bila_{}:\n    p({})\n    v[{}]".format(self.id, self.point, self.velocity)
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