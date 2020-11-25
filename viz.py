# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as plt


def plotGennemsnit(averages: [[float]], years: int):
    # Indlæser gennemsnittene for k = 1 og k = 2
    gennemsnit_k1, gennemsnit_k2 = averages[0], averages[1]

    # parametre for plottet
    plt.style.use("ggplot")
    fig, ax = plt.subplots()
    index = np.arange(years)
    bar_width = 0.35
    opacity = 0.8

    # Plotter bar plots for K = 1 og K = 2
    rects1 = plt.bar(
        index, gennemsnit_k1, bar_width, alpha=opacity, color="tab:blue", label="K=1"
    )

    rects2 = plt.bar(
        index + bar_width,
        gennemsnit_k2,
        bar_width,
        alpha=opacity,
        color="tab:orange",
        label="K=2",
    )

    # labels til plottet
    plt.xlabel("Antal år efter startår")
    plt.ylabel("Gennemsnitlig ventetid")
    plt.title("Sammenligning af ventetider med K antal landingsbaner")
    plt.xticks(index + 0.167, [str(i) for i in range(years)])
    plt.legend()

    # finpudser layout af plot
    plt.tight_layout()

    # gemmer plot som png og viser plottet
    plt.savefig("testplot1.png", dpi=1000)
    plt.show()
