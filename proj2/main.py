import pandas as pd
from Physics import simulation
from matplotlib import pyplot as plt
import numpy as np


def main():
    path = "input.txt"

    data = get_data(path)

    worlds = []
    for i in range(len(data)):
        worlds.append(simulation(i + 1, data[i]))

    for world in worlds:
        print(world)
        draw(world)

    save_output(worlds)




def get_data(path):
    df = pd.read_csv(path, ";", header=None) #reading file

    records = []
    for raw_record in df.values:
        records.append(process(raw_record))

    return records

def process(raw_record):
    location = get_from_brackets(raw_record[0])
    velocity = get_from_brackets(raw_record[-1])
    values = [float(value) for value in raw_record[1:-1]]

    all_values = location
    all_values.extend(velocity)
    all_values.extend(values)
    return all_values


def get_from_brackets(raw_value):
    raw_value = raw_value.replace(" ", "")
    raw_value = raw_value[1:-1]
    values = raw_value.split(",")
    return [float(x) for x in values]

def draw(world, mode="show"):

    #xx = np.linspace(0, world.length, 100)
    #yy = np.linspace(0, world.width, 100)
    xx = [world.puck.x]
    yy = [world.puck.y]
    if len(world.hitted_points) > 0:
        for point in world.hitted_points:
            xx.append(point[0])
            yy.append(point[1])

    xx.append(world.stop_point[0])
    yy.append(world.stop_point[1])

    #plt.figure(num=world.id, figsize=(world.length, world.width))
    axes = plt.gca()
    axes.set_xlim([0, world.length])
    axes.set_ylim([0, world.width])

    plt.title("Symulacja {}".format(world.id), fontsize=28)

    for i in range(1,len(xx) -1):
        plt.scatter(xx[i], yy[i], c='#FF0000', s=100, )

    plt.scatter(xx[0], yy[0], c='#00FF00', s=100)
    plt.scatter(xx[-1], yy[-1], c='#7D0000', s=100)

    plt.plot(xx, yy, c="#0000DD", zorder=0)

    plt.savefig("{}.png".format(world.id))

    plt.clf()

def save_output(worlds):
    with open("output.txt","w+") as f:
        f.seek(0)
        for world in worlds:
            info = []
            if world.fall_out:
                info.append("(out)")
            else:
                info.append("({:.2f},{:.2f})".format(float(world.stop_point[0]), float(world.stop_point[1])))
            info.append("{:.2f}".format(float(world.stop_time)))
            points = []
            for point in world.hitted_points:
                points.append("({:.2f},{:.2f})".format(float(point[0]), float(point[1])))
            info.extend(points)

            line = ";".join(info)
            f.write(line + "\n\n")


if __name__ == "__main__":
    main()