from flights import GenerateFlights

def SimulateAirport(flights: [{}], k: int = 1) -> (int):
    """
    Simulere en lufthavn med k landingsbaner.

    Parameters:
         - flights: [{}], en liste af fly som skal lande i lufthavnen
         - k: int, antal landingsbaner i lufthavnen

    Returns:
         - En tuple af to værdier, flyenes totale vente tid i landingskøen og den højeste vente tid.
    """
    time, dt = 0, 0 # Tidsvariabler brugt under simuleringen
    highestWaitingTime, totalWaitingTime = 0, 0 # Variabler til opbevaring af resultater fra simulering
    queue, airstrips = [], [{"duration": 0, "remainder": 0, "start": 0, "arrival": 0} for _ in range(k)]  # Landingskøen og landingsbanerne

    while len(flights) > 0 or len(queue) > 0:
        # Så længe der er fly der mangler at ankomme eller køen ikke er tom

        # 1. Tjek om der er fly der kan tilføjes til landingskøen
        while (len(flights) > 0 and flights[0]["arrival"] <= time):  # Hvis der er ankomende fly tilføj dem til landingskøen, dette gøres ved hjælp af while løkken
            queue.append(flights.pop(0)) # Fjern flyet fra fly listen og flyt den til køen.

        # 2. Opdater landingsbaner hvis tiden er gået
        for i in range(k):
            if (airstrips[i]["start"] + airstrips[i]["duration"] <= time):  # Tiden er gået, derfor fjernes flyet fra landingsbanen NOTE: Hvis landingsbanen er fri er dette også sandt da 0 + 0 <= time altid gælder.
                timeWaited = airstrips[i]["start"] - airstrips[i]["arrival"] # Den totale tid flyet ventede på en ledig landingsbane NOTE: Denne er 0 hvis der ikke er noget fly på landingsbanen
                totalWaitingTime += timeWaited

                if timeWaited > highestWaitingTime:  # Finder den største ventetid.
                    highestWaitingTime = timeWaited

                # Pop fra køen og lad dette fly lande
                if len(queue) > 0:
                    flight = queue.pop(0)
                    airstrips[i] = {"duration": flight["duration"], "remainder": flight["duration"],"start": time,"arrival": flight["arrival"]}
                else:
                    airstrips[i] = {"duration": 0,"start": 0,"remainder": 0,"arrival": 0} # Landingsbanen forbliver fri

            else:
                airstrips[i]["remainder"] -= dt

        # 3. Opdater tiden der er gået
        dt = min(map(lambda x: x["remainder"], airstrips)) # Finder den mindste remainder og rykker frem i tiden

        time += dt if (dt > 0) else 1

    return (totalWaitingTime, highestWaitingTime)  # Returner en tuple, denne "pakkes ud" når funktionen kaldes

def runSimulations(years: int, days: int, skipYears: int, offset: int) -> [[float]]:
    """
    Driv koden til simuleringerne

    Parameters:
         - years: int, antal år der skal simuleres
         - days: int, antal dage der skal simuleres pr. år.
         - skipYears: int, antal år imellem hver simulering.
         - offset: int, ligges til hvert flys landings varrighed for at simulere dårligt vejr ext.

    Returns:
         - En tuple af to lister, gennemsnittene og de højeste vente tider.
    """

    averages, highest = [], []

    for k in range(1, 3):  # Simuler med 1 og 2 landingsbaner
        dataForK = {"average": [], "highest": []}  # Gennemsnittene og højeste ventetid for k landingsbaner

        for i in range(0, years, skipYears):  # Simuler hvert år
            totalTimeWaiting, highestWaitThisYear = 0, 0

            for _ in range(days):  # For hvert år køres simuleringen 10 gange for at få et mere uniformt billede (nogle dage kan tilfældigvis være meget værre end andre)
                flights = sorted(GenerateFlights(offset=offset, year=i, operationalTime=46800), key=lambda x: x["arrival"])  # Generer tilfældige fly og sortere dem efter ankomst
                wait, highestWaitThisDay = SimulateAirport(flights, k=k)  # Denne funktion returnere en tuple som bliver pakket ud i variablerne wait og heighestWait, hvilket skal forståes som wait = tuple[0] og heighestWait = tuple[1]
                totalTimeWaiting += wait

                # Opdatere den højeste vægt denne dag
                if highestWaitThisDay > highestWaitThisYear:
                    highestWaitThisYear = highestWaitThisDay

            dataForK["average"].append(totalTimeWaiting / days) # Tilføj den gennemsnitlige vente tid pr dag.
            dataForK["highest"].append(highestWaitThisYear) # Tilføj den højeste vente tid.

        averages.append(dataForK["average"]) # Tilføjer alle gennemsnit til average matricen
        highest.append(dataForK["highest"]) # Tilføjer alle de højeste værdier til highest matricen

    return (averages, highest)  # Returner data fra simuleringerne


if (__name__ == "__main__"):
    # Prøv eksemplet fra oplægget.
    flights = [{"arrival": 5, "duration": 15}, {"arrival": 25, "duration": 35}, {"arrival": 50, "duration": 30}, {"arrival": 100, "duration": 20}]
    if (SimulateAirport(flights, k=1)[0] != 10): # Cheker om der er et fly der venter 10 sekunder, ligesom i eksemplet, hvis der ikke er virker koden ikke.
        print("Koden virker ikke...")
    else:
        print("koden virker :)")
