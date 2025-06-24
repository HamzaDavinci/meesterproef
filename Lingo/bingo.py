import random
from colorama import Fore, Style

def genereer_bingo_kaart(even=True):
    nummers = random.sample(
        [i for i in range(2, 100, 2)] if even else [i for i in range(1, 100, 2)],
        16
    )
    return [[str(nummers[i * 4 + j]) for j in range(4)] for i in range(4)]

def update_bingo_kaart(kaart, bal):
    for i in range(4):
        for j in range(4):
            if kaart[i][j] == str(bal):
                kaart[i][j] = Fore.CYAN + str(bal) + Style.RESET_ALL

def check_bingo(kaart):
    for rij in kaart:
        if all(isinstance(cel, str) and Style.RESET_ALL in cel for cel in rij):
            return True

    for kolom in range(4):
        if all(isinstance(kaart[rij][kolom], str) and Style.RESET_ALL in kaart[rij][kolom] for rij in range(4)):
            return True

    if all(isinstance(kaart[i][i], str) and Style.RESET_ALL in kaart[i][i] for i in range(4)):
        return True
    if all(isinstance(kaart[i][3 - i], str) and Style.RESET_ALL in kaart[i][3 - i] for i in range(4)):
        return True

    return False

def toon_bingo_kaart(team, kaart):
    print(f"\nBingo-kaart voor {team}:")
    for rij in kaart:
        regel = " | ".join(cel if cel else " " for cel in rij)
        print(regel)
