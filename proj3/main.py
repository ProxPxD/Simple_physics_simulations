import pandas as pd
from matplotlib import pyplot as plt

from Table import Table
from Ball import Ball


def main():
    path = "input.txt"

    data = get_data(path)

    worlds = []
    for i in range(len(data)):
        worlds.append(Table(i + 1, data[i]))

    for world in worlds:
        #print(world)
        world.simulate()

    for world in worlds:
        draw(world)

    save_output(worlds)




def get_data(path):
    df = pd.read_csv(path, ";", header=None) #reading file

    records = []
    for raw_record in df.values:
        records.append(process(raw_record))

    return records

def process(raw_record):
    all_values = []
    all_values.append(get_from_brackets(raw_record[0]))
    all_values.append(get_from_brackets(raw_record[1]))
    all_values.append(get_from_brackets(raw_record[2]))

    return all_values


def get_from_brackets(raw_value):
    raw_value = raw_value.replace(" ", "")
    raw_value = raw_value[1:-1]
    values = raw_value.split(",")
    return [float(x) for x in values]

def draw(world, mode="show"):

    xx = [[world.starting_points[0].get_x()], [world.starting_points[1].get_x()]]
    yy = [[world.starting_points[0].get_y()], [world.starting_points[1].get_y()]]

    vxx = [[world.starting_velocities[0].get_x()], [world.starting_velocities[1].get_x()]]
    vyy = [[world.starting_velocities[0].get_y()], [world.starting_velocities[1].get_y()]]

    axes = plt.gca()
    r = world.balls[0].get_r()
    axes.set_xlim([0 - r, world.length + r])
    axes.set_ylim([0 - r, world.width + r])

    plt.title("Symulacja {}".format(world.id), fontsize=28)

    for i in range(len(world.balls)):
        x = [world.starting_points[i].get_x()]
        y = [world.starting_points[i].get_y()]
        vx = [world.starting_velocities[i].get_x()]
        vy = [world.starting_velocities[i].get_y()]
        for col in world.balls[i].collsion_points:
            x.append(col[0].get_x())
            y.append(col[0].get_y())
            vx.append(col[1].get_x())
            vy.append(col[1].get_y())

        x.append(world.balls[i].get_point().get_x())
        y.append(world.balls[i].get_point().get_y())
        vx.append(world.balls[i].get_velocity().get_x())
        vy.append(world.balls[i].get_velocity().get_x())

        if i == 0:
            start = '#DDDDDD'
            collision = '#AAAAAA'
            end = '#8A8A8A'
        else:
            start = '#8F8F22'
            collision = '#FFFF00'
            end = '#8F8F00'

        if vx[0] + vy[0] != 0:
            plt.quiver(x[0], y[0], vx[0], vy[0])
        plt.scatter(x[0], y[0], c=start, s=100)
        for j in range(1, len(world.balls[i].collsion_points)-1):
            if vx[j] + vy[j] != 0:
                plt.quiver(x[j], y[j], vx[j], vy[j], angles='xy', scale_units='xy')
            plt.scatter(x[j], y[j], c=collision, s=100)

        plt.scatter(x[-1], y[-1], c=end, s=80)

        plt.plot(x, y, c="#0000DD", zorder=0)

    plt.savefig("{}.png".format(world.id))

    plt.clf()

def save_output(worlds):
    with open("output.txt","w+") as f:
        f.seek(0)
        for world in worlds:
            white_ball = world.balls[0]
            color_ball = world.balls[1]
            info = []
            info.append("({})".format(white_ball.get_point()))
            info.append("({})".format(color_ball.get_point()))
            balls_collisions = world.balls[0].get_counter()
            info.append("{}".format(balls_collisions))
            info.append("{}".format(len(white_ball.collsion_points) - balls_collisions))
            info.append("{}".format(len(color_ball.collsion_points) - balls_collisions))

            line = ";".join(info)
            f.write(line + "\n")


if __name__ == "__main__":
    main()