from Ball import Ball, Point
import copy
import math

class Table:

    def __init__(self, id, record):
        self.id = id
        self.length = 2.7
        self.width = 1.35
        self.mu = 0.015
        self.g = 9.81
        self.energy_remain = 0.7
        self.velocity_remain = self.energy_remain ** 0.5

        self.pocket_radius = 10**(-1)
        self.pockets = [
            Ball(0, 0, 0, 0, 0.1),
            Ball(0, self.length, 0, 0, 0, 0.1),
            Ball(self.width, self.length, 0.1),
            Ball(self.width, 0, 0, 0, 0, 0.1),
            Ball(0, self.length / 2, 0, 0, 0, 0.1),
            Ball(self.width, self.length / 2, 0, 0, 0, 0.1)
        ]

        self.step = 5*10**(-4)
        self.delta = 5*10**(-4)

        [x, y] = record[0]
        [vx, vy] = record[1]
        [x2, y2] = record[2]

        self.balls = [Ball(1, x, y, vx, vy), Ball(2, x2, y2)]
        self.starting_points = [copy.deepcopy(self.balls[0].get_point()), copy.deepcopy(self.balls[1].get_point())]
        self.starting_velocities = [copy.deepcopy(self.balls[0].get_velocity()), copy.deepcopy(self.balls[1].get_velocity())]


    def get_id(self):
        return self.id

    def is_moving(self, velocities):
        return sum([vel.get_length() for vel in velocities]) > self.delta

    def simulate(self):
        velocities = [ball.get_velocity() for ball in self.balls]
        t_c = 0

        while(self.is_moving(velocities)):
            t_c += self.step

            for ball in self.balls:
                if not ball.check_if_fall_out():
                    self.set_attributes(ball, self.step)
                    self.perform_band_collision(ball)
                    self.perform_ball_collision(ball)
                    self.pocket_falling(ball)

    def set_attributes(self, ball, step):
        x = ball.get_point().get_x()
        y = ball.get_point().get_y()
        vel = ball.get_velocity()
        vx = vel.get_x()
        vy = vel.get_y()

        new_vx = 0
        new_vy = 0
        new_x = x
        new_y = y

        a = -self.g * self.mu

        if abs(vx) > self.delta:
            new_x = x + vx*step + (a*step**2)/2

            new_vx = vx + a*step

        if abs(vy) > self.delta:
            new_y = y + vy * step + (a * step ** 2) / 2
            new_vy = vy + a * step

        ball.set_point(new_x, new_y)
        ball.set_velocity(new_vx, new_vy)

        ball.check_distance()

    def perform_band_collision(self, ball):
        x = ball.get_point().get_x()
        y = ball.get_point().get_y()
        vx = ball.get_velocity().get_x()
        vy = ball.get_velocity().get_y()

        colided = False

        r = ball.get_r()

        if vx > 0 and x + r >= self.length:
            vx = -vx * self.velocity_remain
            vy = vy * self.velocity_remain
            colided = True
        elif vx < 0 and x - r <= 0:
            vx = -vx * self.velocity_remain
            vy = vy * self.velocity_remain
            colided = True

        if vy < 0 and y - r <= 0:
            vy = -vy * self.velocity_remain
            vx = vx * self.velocity_remain
            colided = True
        elif vy > 0 and y + r >= self.width:
            vy = -vy * self.velocity_remain
            vx = vx * self.velocity_remain
            colided = True

        if colided:
            ball.set_velocity(vx, vy)
            ball.append_collision()

    def perform_ball_collision(self, ball):
        for ball_2 in self.balls:
            if ball.get_id() != ball_2.get_id():

                if (ball & ball_2) and len(ball.colided) == 0 and len(ball_2.colided) == 0:
                    self.calculate_velocities(ball, ball_2)

                    ball.append_collision(ball_2)
                    ball_2.append_collision(ball)

    def pocket_falling(self, ball):
        point = ball.get_point()
        for pocket in self.pockets:
            if abs(pocket.get_point() - point) < pocket.get_r():
                ball.set_velocity(0, 0)
                ball.set_fall_out()
                x = pocket.get_point().get_x()
                y = pocket.get_point().get_y()
                ball.set_point(x, y)
                break

    def calculate_velocities(self, b1, b2):
        v1 = b1.get_velocity()
        v2 = b2.get_velocity()

        x1 = b1.get_point()
        x2 = b2.get_point()

        m1 = b1.get_m()
        m2 = b1.get_m()

        new_v1 = v1 - 2*m2/(m1+m2) * ((v1-v2)*(x1-x2))/(abs(x1-x2)**2) * (x1-x2)
        new_v2 = v1 - 2*m1/(m1+m2) * ((v2-v1)*(x2-x1))/(abs(x2-x1)**2) * (x2-x1)

        b1.set_velocity(new_v1.x, new_v1.y)
        b2.set_velocity(new_v2.x, new_v2.y)

    def velocity_collision(self, v1, v2, m1, m2):
        return (v1*(m1 - m2) + 2*m2*v2 )/(m1 + m2)

    def __str__(self):
        string = "Stół_{}\n{}\n{}\n".format(self.id, self.balls[0], self.balls[1])
        return string