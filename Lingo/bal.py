import random
from colorama import Fore

def grabbel_bal(teamnaam, ballenbak):
    if not ballenbak:
        print(Fore.RED + f"De ballenbak van {teamnaam} is leeg! Het spel is afgelopen.")
        return None
    index = random.randint(0, len(ballenbak) - 1)
    return ballenbak.pop(index)
