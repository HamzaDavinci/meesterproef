from colorama import Fore
from bingo import check_bingo

def check_win_voorwaarden(team, score, kaart):
    if score["groene_ballen"] >= 3:
        print(Fore.GREEN + f"{team} heeft 3 groene ballen getrokken en wint het spel!")
        return True
    if check_bingo(kaart):
        print(Fore.GREEN + f"{team} heeft een lijn op de bingo-kaart en wint het spel!")
        return True
    if score["goed_geraden"] >= 10:
        print(Fore.GREEN + f"{team} heeft 10 woorden goed geraden en wint het spel!")
        return True
    return False

def check_verlies_voorwaarden(team, score):
    if score["rode_ballen"] >= 3:
        print(Fore.RED + f"{team} heeft 3 rode ballen getrokken en verliest het spel!")
        return True
    if score["fout_ballen"] >= 3:
        print(Fore.RED + f"{team} heeft 3 woorden op rij fout geraden en verliest het spel!")
        return True
    return False
