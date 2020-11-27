from simulation import runSimulations
from viz import plotData
from time import time
import numpy as np

print("Hvis du ønsker at køre koden for at teste om den virker anbefalder vi instillingerne: \n - År: 5,\n - skipYears: 1,\n - Dage pr år: 10,\n - offset: 0")
years = int(input("Antal år, efter år 0: ")) + 1 # Pluser med 1 så 
skipYears = int(input("Hvor mange år vil du have imellem hver simulering? "))
days = int(input("Antal dage der skal simuleres pr år: "))
offset = int(input("Offset, bruges til at simulere dårligt landingsvejr og er en konstant der ligges til hvert flys landingsvarrighed. Sæt denne vaerdi til 0, ved almindeligt vejr... "))
print("\nPåbegynder simulering...") # Så det kan ses at simuleringen går igang da den kan tage langt tid.

start = time()
average, highest = runSimulations(years, days, skipYears, offset)  # Denne funktion returnere en tuple denne bliver derfor pakket ud i to variabler

print("Det tog {0} sekunder...".format(time() - start)) # Tiden simuleringen tog.

# Plotter data fra simuleringen
plotData(1 / 60 * np.array(average), years, skipYears, ("Total ventetid pr dag", "Antal år", "Gennemsnitlig total ventetid i minutter"))
plotData(1 / 60 * np.array(highest), years, skipYears, ("Højeste ventetid pr år", "Antal år", "Højeste ventetid i minutter"))

# Beregner gennemsnitlig vente tid pr fly udfra variablen average.
averagePrFlight = [[avrg / (60 * 200 * np.power(1.05, year)) for avrg, year in zip(average[k], range(0, years, skipYears))] for k in range(2)] # Beregner gennemsnitet pr fly pr år.
plotData(averagePrFlight, years, skipYears, ("Gennemsnitlig ventetid pr fly", "Antal år", "Gennemsnitlig ventetid pr fly i minutter"))
