import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

with open("data\\calibration\\calibration.txt") as fl:
    length_sm = int(fl.readline().split()[1])
    length_steps = int(fl.readline().split()[1])
    # print(length_sm, length_steps)
    K = length_steps / length_sm
    # x = []
    # y = []
    # for i in range(length_sm):
    #     x.append(i)
    #     y.append(i*K)
    _, ax = plt.subplots()
    ax.yaxis.set_major_locator(ticker.MultipleLocator(100))
    ax.plot([0, length_sm], [0, length_steps])
    ax.grid(True)
    ax.text(4,400, f"K = {K} st/sm")
    plt.title("График зависимости пройденного корреткой \nрасстояния от количества шагов мотора")
    plt.show()