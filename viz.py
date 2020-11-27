import numpy as np
import matplotlib.pyplot as plt


def plotData(data: [[float]], years: int, skipYears: int, labels: (str)):
    """

    Plotter data:

    Parameter:
         - Data: [[float]], en matrix hvor hver række er data fra en landingbane med henholdsvis 1 og 2 landingsbaner.
         - Years: int, antal år.
         - skipYears: int, benyttes til x koordinater.
         - labels: (str), en tupel af string som bruges til aksetitler med mere.

    """

    # Indlæser gennemsnittene for k = 1 og k = 2
    data_k1, data_k2 = data[0], data[1]

    # parametre for plottet
    plt.style.use("ggplot")
    fig, ax = plt.subplots()
    index = np.arange(0, years, skipYears)
    bar_width = 0.35
    opacity = 0.8

    # Plotter bar plots for K = 1 og K = 2
    plt.bar(
        index,
        data_k1,
        bar_width,
        alpha=opacity,
        color="tab:blue",
        label="K=1"
    )

    plt.bar(
        index + bar_width,
        data_k2,
        bar_width,
        alpha=opacity,
        color="tab:orange",
        label="K=2"
    )

    # labels til plottet
    plt.xlabel(labels[1])
    plt.ylabel(labels[2])
    plt.title(labels[0])
    plt.xticks(index + 0.167, [str(i) for i in range(0, years, skipYears)])
    plt.legend()

    # finpudser layout af plot
    plt.tight_layout()

    # gemmer plot som png og viser plottet
    plt.savefig("testplot1.png", dpi=1000)
    plt.show()
