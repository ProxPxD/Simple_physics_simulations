import math

class simulation:


    def __init__(self, id, record):
        self.id = id

        self.g = 10
        self.length = 60
        self.width = 40
        self.hole_length = 1
        self.step = 10**(-3)
        self.delta = 10**(-4)

        self.times_of_hits = []
        self.stop_time = -1
        self.stop_point = []
        self.hitted_points = []
        self.stop_point = []

        self.mi = record[-1]

        record.pop(-1)
        self.puck = self.__Puck(id, record)

        self.alpha = math.atan2(self.puck.v_y, self.puck.v_x)
        self.a = -(self.g * self.mi)
        self.a_x = self.a * math.cos(self.alpha)
        self.a_y = self.a * math.sin(self.alpha)

        self.fall_out = False
        self.stop_time = self._get_points()


    def _get_points(self):
        r = self.puck.radius

        x_0 = self.puck.x
        y_0 = self.puck.y

        v = v_0 = self.puck.v

        vx = vx_0 = self.puck.v_x
        vy = vy_0 = self.puck.v_y

        a = self.a
        ax = self.a_x
        ay = self.a_y

        x_right = vx > 0
        y_up = vy > 0

        t_c = 0

        times = []
        hitted = []

        length = len(times)
        time = 0

        x = distance(t_c, x_0, vx_0, ax)
        y = distance(t_c, y_0, vy_0, ay)

        while (v >= self.delta):
            t_c += self.step

            x = distance(t_c, x_0, vx_0, ax)
            y = distance(t_c, y_0, vy_0, ay)

            v = velocity(t_c, v_0, a)
            vx = velocity(t_c, vx_0, ax)
            vy = velocity(t_c, vy_0, ay)

            if x_right and x + r >= self.length:
                time += t_c
                times.append(time)
                if x > self.length:
                    x = self.length
                hitted.append([x,y])
                x_right = False
                vx = -vx

            elif not x_right and x - r <= 0:
                time += t_c
                times.append(time)
                if x < 0:
                    x = 0.0
                hitted.append([x,y])
                x_right = True
                vx = -vx

            elif y_up and y + r >= self.width:
                mid = self.length/2.0
                half = self.hole_length/2.0
                if mid - half < x < mid + half:
                    self.fall_out = True
                    break
                else:
                    time += t_c
                    times.append(time)
                    if y > self.width:
                        y = self.width
                    hitted.append([x,y])
                    y_up = False
                    vy = -vy

            elif not y_up and y - r <= 0:
                mid = self.length
                half = self.hole_length / 2
                if mid - half < x < mid + half:
                    self.fall_out = True
                    break
                else:
                    time += t_c
                    times.append(time)
                    if y < 0:
                        y = 0.0
                    hitted.append([x,y])
                    y_up = True
                    vy = -vy

            if length < len(times):
                x_0 = x
                y_0 = y

                x_0 = 0 if x_0 < 0 else x_0
                y_0 = 0 if y_0 < 0 else y_0

                x_0 = self.length if x_0 > self.length else x_0
                y_0 = self.width if y_0 > self.width else y_0

                vx_0 = vx
                vy_0 = vy
                v_0 = velocity(t_c, v_0,a)

                t_c = 0
                length = len(times)

        self.times_of_hits = times
        self.hitted_points = hitted

        stop_time = time + t_c

        self.stop_point = [x,y]


        return stop_time


    def get_velocity(self, t, axis='x'):
        v_0 = 0

        if axis == 'x':
            v_0 = self.puck.v_x
        elif axis == 'y':
            v_0 = self.puck.v_y

        t_c = 0 #current time
        v = v_0
        a = -self.mi * self.g
        while(v > 0 or t_c < t):
            t_c += self.step
            v = velocity(t_c, v_0, a)

        if v < 0:
            return 0
        return v

    def get_distance(self, t, axis='x'):
        s_0 = 0
        v_0 = 0

        if axis == 'x':
            s_0 = self.puck.x
            v_0 = self.puck.v_x
        elif axis == 'y':
            v_0 = self.puck.v_y
            s_0 = self.puck.y

        t_c = 0  # current time

        s = s_0
        v = v_0
        a = -self.mi * self.g
        while (v > 0 or t_c < t):
            t_c += self.step
            s = distance(t_c, s_0, v_0, a)
            v = velocity(t_c, v_0, a)

        if v < 0:
            return 0
        return v

    def __str__(self):
        simulation_string = "Simulation_{}\n".format(self.id)
        simulation_string += "  μ = {}\n".format(self.mi)
        simulation_string += "  times of hits: {}\n".format(self.times_of_hits)
        simulation_string += "  hitted points: {}\n".format(self.hitted_points)
        simulation_string += "  stop time: {}\n".format(self.stop_time)
        simulation_string += "  stop point: {}\n".format(self.stop_point)

        simulation_string += str(self.puck)

        return simulation_string

    class __Puck:

        x = 0
        y = 0
        mass = 0
        radius = 0
        v_x = 0
        v_y = 0

        def __init__(self, id, record):
            self.id = id
            self.x = record[0]
            self.y = record[1]
            self.v_x = record[2]
            self.v_y = record[3]
            self.v = (self.v_x**2 + self.v_y**2)**0.5
            self.mass = record[4]
            self.radius = record[5]

        def __str__(self):
            puck_string = " -Puck_{}\n".format(self.id)
            puck_string += "   (x,y): ({},{})\n".format(self.x, self.y)
            puck_string += "   [vx,vy]: [{},{}]\n".format(self.v_x, self.v_y)
            puck_string += "   m = {}\n   r = {}\n".format(self.mass, self.radius)
            return puck_string


def distance(t, s_0, v_0, a):
    return s_0 + v_0*t + (a*t**2)/2

def velocity(t, v_0, a):
    return v_0 + a*t