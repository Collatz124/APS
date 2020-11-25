from test import GenerateFlights
import time as t
# from viz import plotData


def SimulateAirport(k: int = 1, offset: int = 0, year: int = 0, operationalTime: int = 46800):
    """ Simulere en lufthavn med k landingsbaner """
    flights = sorted(
        GenerateFlights(offset=offset, year=year, oT=operationalTime),
        key=lambda x: x["arrival"],
    )  # Generer tilfældige fly og sortere dem efter ankomst

    time, dt, totalWaitingTime = 0, 0, 0
    heighestWaitingTime = 0
    queue, airstrips = [], [{"duration": 0, "remainder": 0, "start": 0, "arrival": 0} for _ in range(k)]  # Landingskøen og landingsbanerne

    while len(flights) > 0 or len(queue) > 0:
        # Så længe der er fly der mangler at ankomme eller køen ikke er tom

        # 1. Tjek om der er fly der kan tilføjes til landingskøen
        while (len(flights) > 0 and flights[0]["arrival"] <= time):  # Hvis der er ankomende fly tilføj dem til landingskøen
            queue.append(flights.pop(0))

        # 2. Opdater landingsbaner hvis tiden er gået
        for i in range(k):
            if (airstrips[i]["start"] + airstrips[i]["duration"] <= time):  # Tiden er gået, derfor fjernes flyet fra landingsbanen NOTE: Hvis landingsbanen er fri er dette også sandt da 0 + 0 <= time altid gælder.
                timeWaited = airstrips[i]["start"] - airstrips[i]["arrival"]
                # Den totale tid flyet ventede på en ledig landingsbane
                totalWaitingTime += timeWaited
                if timeWaited > heighestWaitingTime:  # Finder den største ventetid.
                    heighestWaitingTime = timeWaited

                # Pop fra køen og lad dette fly lande
                if len(queue) > 0:
                    flight = queue.pop(0)
                    airstrips[i] = {
                        "duration": flight["duration"],
                        "remainder": flight["duration"],
                        "start": time,
                        "arrival": flight["arrival"]
                    }
                else:
                    airstrips[i] = {
                        "duration": 0,
                        "start": 0,
                        "remainder": 0,
                        "arrival": 0
                    }

            else:
                airstrips[i]["remainder"] -= dt

        # 3. Opdater tiden der er gået
        dt = sorted(airstrips, key=lambda x: x["remainder"])[0]["remainder"]  # Finder den mindste remainder og rykker frem i tiden

        time += dt if (dt > 0) else 1

    return (totalWaitingTime, heighestWaitingTime)  # Returner en tuple, denne "pakkes ud" når funktionen kaldes


def runSimulations(years: int):
    """ Runs simulations of the airports """
    avarges, maximumTimeWaiting = [], []
    highestWaitingTimePerYear = [[0, 0] for _ in range(years)]
    for k in range(1, 3):  # Simuler med 1 og 2 landingsbaner
        avargesForK = []  # Gennemsnittene for k landingsbaner

        for i in range(years):  # Simuler hvert år
            totalTimeWaiting = 0

            for _ in range(365):  # For hvert år køres simuleringen 10 gange for at få et mere uniformt billede (nogle dage kan tilfældigvis være meget værre end andre)
                wait, highestWait = SimulateAirport(k=k, offset=0, year=i, operationalTime=46800)  # Denne funktion returnere en tuple som bliver pakket ud i variablerne wait og heighestWait, hvilket skal forståes som wait = tuple[0] og heighestWait = tuple[1]
                totalTimeWaiting += wait
                if highestWait > highestWaitingTimePerYear[i][k - 1]:
                    highestWaitingTimePerYear[i][k - 1] = highestWait

            avargesForK.append(totalTimeWaiting / 365)  # Tilføj den gennemsnitlige vente tid.

        avarges.append(avargesForK)

    return (avarges, highestWaitingTimePerYear)  # Returner data fra simuleringerne


if __name__ == "__main__":
    # Dette kode køre simuleringen
    years = int(input("Antal år: "))

    start = t.time()
    gennemsnit, heighest = runSimulations(years)  # Denne funktion returnere en tuple denne bliver derfor pakket ud i to variabler
    print("Det tog {0} sekunder...".format(t.time() - start))
    print(gennemsnit, heighest)
    #plotData(gennemsnit, years, ("Gennemsnitlig ventetid i en lufthavn med K landingsbaner.", "Antal år", "Gennemsnitlig ventetid i sekunder"))
    #plotData(heighest, years, ("Højeste ventetid i en lufthavn med K landingsbaner.", "Antal år", "Højeste ventetid i sekunder"))
