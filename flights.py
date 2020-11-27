import numpy as np


def GenerateLandingDuration():
    """ Genere en landings tid baseret på det givne data fra oplægget. """
    dist = (0, 16, 33, 61, 41, 25, 10, 8, 6, 0)  # Hvert index repreæsentere en landingstid i sekunder 0: 0-30, 1: 31-60 osv.

    randomNumber = np.random.randint(0, sum(dist) + 1)  # Genenere et tilfældigt tal, for at finde ud af i hvilket område flyets landings tid skal ligge
    for i in range(len(dist)):
        if randomNumber >= sum(dist[:i]): # Hvis det tilfældige tal lige har været i sum(dist[:i]) generes et tilfældigt tal nedenfor
            return np.random.randint(30 * i + 1 if (i > 0) else 0, 30 * (i + 1))  # Tager højde for at distruptionen kan ændre sig så der kommer fly med landingstider på 0-30 sekunder


def GenerateFlights(offset: int = 0, year: int = 0, oT: int = 46800):
    """

    Parameter:
        - offset: int, offset som lægges til alle landings varigheder.
        - year: int, antal år siden år 0.
        - oT: int, tiden på en dag.

    Return:
        - En liste af fly, repræsenteret af dictonaries.

    """

    n = int(round(200 * np.power(1.05, year)))  # Antalet af fly vokser med 5% hvert år, NOTE Dette laves om til et heltal da der ikke kan være et halvt fly ;)

    flights = []

    for _ in range(n):
        duration = GenerateLandingDuration() + offset  # Flyets landings periode
        arrival = np.random.randint(0, oT)  # Flyet ankomst imellem 0 og oT

        flights.append({"arrival": arrival, "duration": duration})

    return flights

if (__name__ == "__main__"):
    """ Test kode til dette modul """
    # Test af GennerateFlights
    flights = GenerateFlights(year = 1) # Bør gennere 210 fly, da 200 * 1.05.
    print(len(flights)) # Tjekker om der rent faktisk er 210 fly.
    print(flights[0]) # Printer det første fly. 