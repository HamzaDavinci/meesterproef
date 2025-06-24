import unittest
from colorama import Fore, Style
import random

from Lingo import *  # Zorg dat deze functies beschikbaar zijn in Lingo.py: woord_splitter, kleur_letters, genereer_bingo_kaart

class TestLingoFunctions(unittest.TestCase):

    # Test of een woord correct gesplitst wordt in losse letters
    def test_woord_splitter(self):
        self.assertEqual(woord_splitter("taart"), ['t', 'a', 'a', 'r', 't'])

    # Test of alle letters exact goed gekleurd worden als het woord 100% correct is
    def test_kleur_letters_exact(self):
        resultaat = kleur_letters("taart", "taart")
        verwacht = Fore.GREEN + 't' + Fore.GREEN + 'a' + Fore.GREEN + 'a' + Fore.GREEN + 'r' + Fore.GREEN + 't'
        self.assertEqual(resultaat.replace(Style.RESET_ALL, ''), verwacht)

    # Test of kleuring klopt als sommige letters juist of fout zijn
    def test_kleur_letters_partial(self):
        resultaat = kleur_letters("raast", "taart")
        self.assertIn(Fore.YELLOW + 'r', resultaat)
        self.assertIn(Fore.GREEN + 'a', resultaat)
        self.assertIn(Fore.GREEN + 't', resultaat)

    # Test of gegenereerde bingo-kaart alleen even getallen bevat
    def test_genereer_bingo_kaart_even(self):
        kaart = genereer_bingo_kaart(True)
        for rij in kaart:
            for cel in rij:
                self.assertTrue(int(cel) % 2 == 0)

    # Test of gegenereerde bingo-kaart alleen oneven getallen bevat
    def test_genereer_bingo_kaart_oneven(self):
        kaart = genereer_bingo_kaart(False)
        for rij in kaart:
            for cel in rij:
                self.assertTrue(int(cel) % 2 == 1)

    # Test of bingo gedetecteerd wordt als een volledige rij aangekruist is
    def test_bingo_detectie(self):
        kaart = [[Fore.CYAN + str(i) + Style.RESET_ALL for i in range(4)]]
        kaart += [[str(i) for i in range(4)] for _ in range(3)]
        bingo = check_bingo_custom(kaart)
        self.assertTrue(bingo)

    # Test of een specifiek getal goed wordt aangepast (aangestreept) op de kaart
    def test_update_bingo_kaart(self):
        kaart = [[str(i + j * 4) for i in range(4)] for j in range(4)]
        update_bingo_kaart_custom(kaart, 5)
        gevonden = False
        for rij in kaart:
            for cel in rij:
                if cel.startswith(Fore.CYAN) and "5" in cel:
                    gevonden = True
        self.assertTrue(gevonden)

# Simpele versie van bingo-checker om los te testen zonder volledige game-logica
def check_bingo_custom(kaart):
    for rij in kaart:
        if all(isinstance(c, str) and Style.RESET_ALL in c for c in rij):
            return True
    for col in range(4):
        if all(isinstance(kaart[row][col], str) and Style.RESET_ALL in kaart[row][col] for row in range(4)):
            return True
    if all(Style.RESET_ALL in kaart[i][i] for i in range(4)):
        return True
    if all(Style.RESET_ALL in kaart[i][3 - i] for i in range(4)):
        return True
    return False

# Past 1 waarde aan op de kaart als het overeenkomt met de getrokken bal
def update_bingo_kaart_custom(kaart, bal):
    for i in range(4):
        for j in range(4):
            if kaart[i][j] == str(bal):
                kaart[i][j] = Fore.CYAN + str(bal) + Style.RESET_ALL

if __name__ == '__main__':
    unittest.main()
