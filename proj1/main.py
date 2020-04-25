import pandas as pd
from Physic import *

from matplotlib import pyplot as plt
import numpy as np

'''
    W moim programie założyłem,
    że wiatr jest przyśpieszniem
    ~ Piotr Maliszewski 
'''


def main():

    throws = load_data("input.txt")

    for throw in throws:
        draw(throw, "show")
        draw(throw, "save")

    save_calculations("output.txt", throws)


def draw(throw, mode="show"):
    x_array = [throw.cannon.x, throw.target.x, throw.hitted_point.x]
    x_array.extend([throw.distance_x(time) for time in throw.times_array])

    x_min = min(x_array)
    x_max = max(x_array)

    d = (x_max - x_min)/4
    r = np.linspace(x_min - d/2, x_max + d / 2, 100)
    t = np.linspace(0, throw.end_time, 100)

    gain = 0.4*0

    #plt.axis("off")
    plt.title("Rzut {}".format(throw.id), fontsize=28)

    #Land
    plt.fill_between(r, throw.function(r) + gain, facecolor='#00FF00', zorder=0)

    #throw
    plt.plot(throw.distance_x(t), throw.distance_y(t) + gain, c="#AAAAAA", zorder=0)

    plt.scatter(throw.cannon.x, throw.cannon.y + gain, c='#0000FF', s=100)
    plt.scatter(throw.target.x, throw.target.y + gain, c='#FF0000', s=100)
    plt.scatter(throw.hitted_point.x, throw.hitted_point.y + gain, c='#DD0000', s=60, marker="x")

    for point in throw.points_in_times:
        if point.y > throw.function(point.x):
            plt.scatter(point.x, point.y + gain, c='#0000EE', s=60, marker="+")

    plt.quiver(throw.cannon.x, throw.cannon.y + gain, throw.initial_velocity.x + gain, throw.initial_velocity.y, facecolor="#000044")

    if mode == "show":
        plt.show()
    elif mode == "save":
        plt.savefig("{}.png".format(throw.id))

    plt.clf()


def load_data(location):
    df = pd.read_csv(location, sep=';', header=None,
                     names=["cannon", "target", "velocity", "wind", "time_1", "time_2", "time_3", "function"])

    throws = []
    i = 0
    while(i < len(df.values)):
        record = df.values[i]
        initial_conditions = get_initial_values(record)
        throws.append(Throw(i+1,initial_conditions))
        i += 1
    return throws

def get_initial_values(record):
    initial_conditions = []
    for i in range(len(record)):
        initial_conditions.extend(get_value_from_record(record, i))
    return initial_conditions

def get_value_from_record(record, col):
    if col < 4:
        return get_coordinace(record[col])
    elif col == len(record) - 1:
        # equation
        return [record[col]]
    else:
        return [float(record[col])]


def get_coordinace(ordered_pair_string):
    seperated_numbers = delete_brackets(ordered_pair_string)
    array_of_string_numbers = seperated_numbers.split(',')
    return list(map(float, array_of_string_numbers))

def delete_brackets(string):
    brackets = "()[]{}"
    purified = ""
    for ch in string:
        if ch not in brackets:
            purified += ch

    return purified

def save_calculations(location, throws):
    result = {
        "(x,y)": [],
        "h_max": [],
        "t_1": [],
        "t_2": [],
        "t_3": [],
        "hit": []
    }
    for throw in throws:
        result["(x,y)"].append(str(throw.hitted_point))
        result["h_max"].append("{:.2f}".format(throw.max_hight))
        for i in range(len(throw.times_array)):
            result["t_{}".format(i+1)].append(str(throw.velocity_in_times[i]))
        result["hit"].append(int(throw.has_hitted))

    df = pd.DataFrame(result)

    df.to_csv(location, sep=";", quoting=None)


if __name__ == "__main__":
    main()
