#!/usr/bin/env python3
from simulation import runSimulations
from viz import plotData
from time import time
import numpy as np

years = int(input("Antal år, efter år 0: ")) + 1
skipYears = int(input("Hvor mange år vil du have imellem hver simulering? "))
days = int(input("Antal dage der skal simuleres pr år: "))
offset = int(input("Offset, bruges til at simulere dårligt landingsvejr og er en konstant der ligges til hvert flys landingsvarrighed. Sæt denne værdi til 0, ved almindeligt vejr..."))
print("Påbegynder simulering...") # Så det kan ses at simuleringen går igang da den kan tage langt tid.

start = time()
average, highest = runSimulations(years, days, skipYears, offset)  # Denne funktion returnere en tuple denne bliver derfor pakket ud i to variabler

print("Det tog {0} sekunder...".format(time() - start)) # Tiden simuleringen tog.

# Plotter data fra simuleringen
plotData(average, years, skipYears, ("Gennemsnitlig total ventetid", "Antal år", "Gennemsnitlig totalventetid i sekunder"))
plotData(highest, years, skipYears, ("Højeste ventetid", "Antal år", "Højeste ventetid i sekunder"))

# Beregner gennemsnitlig vente tid pr fly udfra variablen average. TODO: få den her del til at fungere
averagePrFlight = [[avrg / np.power(200, year) for avrg, year in zip(average[k], range(0, years, skipYears))] for k in range(2)] # Beregner gennemsnitet pr fly pr år.
plotData(averagePrFlight, years, skipYears, ("Gennemsnitlig ventetid", "Antal år", "Gennemsnitlig ventetid i sekunder"))
