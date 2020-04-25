from Body import Body, Point
import copy
import math

class World:

    def __init__(self, id, record):
        self.id = id
        self.G = 7.6 * 10**(-11)

        self.step = 5*10**(-1)

        self.time_point = record[0]
        self.time_point_data = []

        self.collisions = []

        record = record[1:]

        self.bodies = []
        self.used_bodies = []

        i = 0
        colors = [[1, 0, 1], [0, 1, 0], [0, 0, 1]]
        for info in record:
            body = Body(i+1, info[0][0], info[0][1], info[1][0], info[1][1], info[2], colors[i])
            self.bodies.append(body)
            i += 1


    def get_bodies(self):
        return self.bodies

    def get_used(self):
        return self.used_bodies

    def get_id(self):
        return self.id

    def moreThanOne(self):
        return len(self.bodies) > 1

    def simulate(self):
        t_c = 0

        got_time = False

        while(self.moreThanOne()):
            t_c += self.step
            if not got_time and t_c > self.time_point:
                got_time = True
                all = self.bodies
                all.extend(self.used_bodies)
                for body in all:
                    self.time_point_data.append(copy.deepcopy(body))

            for body in self.bodies:
                self.set_attributes(body, self.step)
                self.perform_body_collision(body)
                body.add_pos(body.get_point())

        self.used_bodies.append(copy.deepcopy(self.bodies[0]))
        self.bodies.remove(self.bodies[0])


    def set_attributes(self, body, step):

        point = body.get_point()
        vel = body.get_velocity()

        a = Point(0,0)

        for body_2 in self.bodies:
            if body_2.get_id() != body.get_id():
                vec = point - body_2.get_point()
                r = abs(vec)
                a -= self.G*body_2.get_m()*(vec)/r**3

        new_point = point + vel * step
        new_vel = vel + a*step

        body.set_point(new_point)
        body.set_velocity(new_vel)


    def perform_body_collision(self, body):
        for body_2 in self.bodies:
            if body.get_id() != body_2.get_id():

                if body & body_2:
                    self.used_bodies.append(copy.deepcopy(body))
                    self.used_bodies.append(copy.deepcopy(body_2))

                    new_body = body + body_2

                    self.bodies.remove(body)
                    self.bodies.remove(body_2)

                    self.collisions.append(copy.deepcopy(new_body.get_point()))

                    self.bodies.append(new_body)


    def __str__(self):
        string = "Świat_{}\n".format(self.id)
        all = self.bodies
        all.extend(self.used_bodies)
        for body in all:
            string += str(body) + "\n"
        return string