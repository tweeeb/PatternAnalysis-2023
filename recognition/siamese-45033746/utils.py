import os
import random
import matplotlib.pyplot as plt
import datetime


def show_plot(iteration, loss):
    plt.plot(iteration, loss)
    plt.show()
    # plt.savefig(f"./assets/train_loss.png")


def save_plot(iteration, loss):
    with open(f"./assets/iteration_{datetime.datetime.now()}.txt", "w") as output:
        output.write(str(iteration))
    with open(f"./assets/loss_{datetime.datetime.now()}.txt", "w") as output:
        output.write(str(loss))

if __name__ == '__main__':
    data = open("./assets/it.txt", "r")
    info = data.read()
    iter_list = info.replace('\n', '').split(",")
    iter_list = list(map(int, iter_list))
    data.close()

    data = open("./assets/loss.txt", "r")
    info = data.read()
    loss_list = info.replace('\n', '').split(",")
    loss_list = list(map(float, loss_list))
    data.close()

    show_plot(iter_list, loss_list)
