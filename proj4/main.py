import pandas as pd
from matplotlib import pyplot as plt

from World import World
from Body import Body


def main():
    path = "input.txt"

    data = get_data(path)

    worlds = []
    for i in range(len(data)):
        worlds.append(World(i + 1, data[i]))

    for world in worlds:
        print(world)
        world.simulate()
        draw(world)

    save_output(worlds)




def get_data(path):
    df = pd.read_csv(path, ";", header=None) #reading file

    records = []
    for raw_record in df.values:
        records.append(process(raw_record))

    return records

def process(raw_record):
    all_values = [float(raw_record[-1])]
    for i in range(3):
        bodyInfo = []
        bodyInfo.append(get_from_brackets(raw_record[3*i]))
        bodyInfo.append(get_from_brackets(raw_record[3*i+1]))
        bodyInfo.append(float(raw_record[3*i+2]))
        all_values.append(bodyInfo)
        i += 1

    return all_values


def get_from_brackets(raw_value):
    raw_value = raw_value.replace(" ", "")
    raw_value = raw_value[1:-1]
    values = raw_value.split(",")
    return [float(x) for x in values]

def draw(world, mode="show"):

    plt.title("Symulacja {}".format(world.id), fontsize=28)

    bodies = world.get_used()

    for body in bodies:
        xx = []
        yy = []
        for point in body.get_history():
            xx.append(point.x)
            yy.append(point.y)

        plt.scatter(xx, yy, color=body.get_color(), s=40)

    time_data = world.time_point_data

    for body in time_data:
        point = body.get_point()
        plt.scatter(point.x, point.y, c='#FF0000', s=35)

        vec = body.get_velocity()
        #plt.quiver(point.x, point.y, vec.x, vec.y, color=[0, 0, 0], angles='xy', scale_units='xy', scale=50)


    plt.savefig("{}.png".format(world.id))
    plt.show()

    plt.clf()
    plt.close()

def save_output(worlds):
    with open("output.txt","w+") as f:
        f.seek(0)
        for world in worlds:
            info = []
            time_data = world.time_point_data
            for body in time_data:
                info.append("({})".format(body.get_point()))
                info.append("[{}]".format(body.get_velocity()))

            for col in world.collisions:
                info.append("({})".format(col))

            line = ";".join(info)
            f.write(line + "\n")


if __name__ == "__main__":
    main()