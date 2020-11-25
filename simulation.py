from flights import GenerateFlights
from time import time
from viz import plotData


def SimulateAirport(
    k: int = 1, offset: int = 0, year: int = 0, operationalTime: int = 46800
):
    """ Simulere en lufthavn med k landingsbaner """
    flights = sorted(
        GenerateFlights(offset=offset, year=year, oT=operationalTime),
        key=lambda x: x["arrival"],
    )  # Generer tilfældige fly og sortere dem efter ankomst
    time, dt, totalWaitingTime = 0, 0, 0
    queue, airstrips = [], [
        {"duration": 0, "remainder": 0, "start": 0, "arrival": 0} for _ in range(k)
    ]  # Landingskøen

    while len(flights) > 0 or len(queue) > 0:
        # Så længe der er fly der mangler at ankomme eller køen ikke er tom

        # 1. Tjek om der er fly der kan tilføjes til landingskøen
        while (
            len(flights) > 0 and flights[0]["arrival"] <= time
        ):  # Hvis der er ankomende fly tilføj dem til landingskøen
            queue.append(flights.pop(0))

        # 2. Opdater landingsbaner hvis tiden er gået
        for i in range(k):
            if (
                airstrips[i]["start"] + airstrips[i]["duration"] <= time
            ):  # Tiden er gået, derfor fjernes flyet fra landingsbanen
                totalWaitingTime += airstrips[i]["start"] - airstrips[i]["arrival"]

                # Pop fra køen og lad dette fly lande
                if len(queue) > 0:
                    flight = queue.pop(0)
                    airstrips[i] = {
                        "duration": flight["duration"],
                        "remainder": flight["duration"],
                        "start": time,
                        "arrival": flight["arrival"],
                    }
                else:
                    airstrips[i] = {
                        "duration": 0,
                        "start": 0,
                        "remainder": 0,
                        "arrival": 0,
                    }

            else:
                airstrips[i]["remainder"] -= dt

        # 3. Opdater tiden der er gået
        dt = sorted(airstrips, key=lambda x: x["remainder"])[0][
            "remainder"
        ]  # Finder den mindste remainder og rykker frem i tiden

        time += dt if (dt > 0) else 1

    return totalWaitingTime


def runSimulations(years: int):
    """ Runs simulations of the airports """
    avarges, maximumTimeWaiting = [], []
    for k in range(1, 3):  # Simuler med 1 og 2 landingsbaner
        avargesForK = []  # Gennemsnittene for k landingsbaner

        for i in range(years):  # Simuler hvert år
            totalTimeWaiting = 0

            for _ in range(
                365
            ):  # For hvert år køres simuleringen 10 gange for at få et mere uniformt billede (nogle dage kan tilfældigvis være meget værre end andre)
                totalTimeWaiting += SimulateAirport(
                    k=k, offset=0, year=i, operationalTime=46800
                )

            avargesForK.append(
                totalTimeWaiting / 365
            )  # Tilføj den gennemsnitlige vente tid.

        avarges.append(avargesForK)

    return avarges


if __name__ == "__main__":
    # Dette kode køre simuleringen
    years = int(input("Antal år: "))

    start = time()
    data = runSimulations(years)
    print("Det tog {0} ms...".format(time() - start))
    plotData(data, years)
