import numpy as np


def GenerateLandingDuration():
    """ Genere en landings tid baseret på det givet data """
    dist = (0, 16, 33, 61, 41, 25, 10, 8, 6, 0)  # Hvert index repreæsentere en landingstid i sekunder 0: 0-30, 1: 31-60 osv.

    randomNumber = np.random.randint(0, sum(dist) + 1)  # Genenere et tilfældigt tal, for at finde ud af i hvilket område flyets landings tid skal ligge
    for i in range(len(dist)):
        if randomNumber <= sum(dist):
            return np.random.randint(30 * i + 1 if (i > 0) else 0, 30 * (i + 1))  # Tager højde for at distruptionen kan ændre sig så der kommer fly med landingstider på 0-30 sekunder


def GenerateFlights(offset: int = 0, year: int = 0, oT: int = 46800):
    """ Genere en liste af fly """
    n = int(round(200 * np.power(1.05, year)))  # Antalet af fly vokser med 5% hvert år, NOTE Dette laves om til et heltal da der ikke kan være et halvt fly ;)

    flights = []

    for _ in range(n):
        duration = GenerateLandingDuration() + offset  # Flyets landings periode
        arrival = np.random.randint(0, oT)  # Flyet ankomst imellem 0 og oT

        flights.append({"arrival": arrival, "duration": duration})

    return flights
