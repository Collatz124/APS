#!/usr/bin/env python3
from simulation import runSimulations
from viz import plotData
from time import time

years = int(input("Antal år: "))
skipYears = True if (input("vil du skip 5 år adgangen? y/n ") == "y") else False
days = int(input("Antal dage der skal simuleres pr år: "))

print("Påbegynder simulering...") # Så det kan ses at simuleringen går igang da den kan tage langt tid.

start = time()
average, highest = runSimulations(years, days, skipYears)  # Denne funktion returnere en tuple denne bliver derfor pakket ud i to variabler

print("Det tog {0} sekunder...".format(time() - start)) # Tiden simuleringen tog.

# Plotter data fra simuleringen
plotData(average, years, skipYears, ("Gennemsnitlig ventetid i en lufthavn med K landingsbaner.", "Antal år", "Gennemsnitlig ventetid i sekunder"))
plotData(highest, years, skipYears, ("Højeste ventetid i en lufthavn med K landingsbaner.", "Antal år", "Højeste ventetid i sekunder"))
