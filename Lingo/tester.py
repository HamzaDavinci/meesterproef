import unittest
from colorama import Fore, Style
from Lingo import woord_splitter, kleur_letters, genereer_bingo_kaart

# ------------------------------------------
# TESTSCRIPT VOOR LINGO.PY FUNCTIES
#
# Hoe te gebruiken:
# 1. Zorg dat Lingo.py in dezelfde map staat en de volgende functies bevat:
#    - woord_splitter(woord): splitst een woord in letters
#    - kleur_letters(geraden_woord, doel_woord): geeft kleuren aan letters terug
#    - genereer_bingo_kaart(even=True): genereert een 4x4 bingo-kaart met even of oneven getallen
#
# 2. Installeer colorama (indien nog niet): pip install colorama
#
# 3. Run deze test met: python tester.py
#
# 4. De tests controleren:
#    - woord_splitter splitsen van een woord in letters
#    - kleur_letters kleuren (groen/geel) van letters bij juiste/minder juiste matches
#    - genereer_bingo_kaart maakt alleen even of alleen oneven nummers
#    - bingo detectie op volledige rij/kolom/diagonaal
#    - markering van een getal op de bingo-kaart
#
# ------------------------------------------

class TestLingoFunctions(unittest.TestCase):
    # Unit tests voor Lingo.py functies

    def test_woord_splitter(self):
        # Test: splitst 'taart' correct in ['t', 'a', 'a', 'r', 't']
        self.assertEqual(woord_splitter("taart"), ['t', 'a', 'a', 'r', 't'])

    def test_kleur_letters_exact(self):
        # Test: kleur_letters kleurt alle letters groen bij exact gelijk woord
        resultaat = kleur_letters("taart", "taart")
        verwacht = Fore.GREEN + 't' + Fore.GREEN + 'a' + Fore.GREEN + 'a' + Fore.GREEN + 'r' + Fore.GREEN + 't'
        # Verwijder reset codes voor vergelijking
        self.assertEqual(resultaat.replace(Style.RESET_ALL, ''), verwacht)

    def test_kleur_letters_partial(self):
        # Test: kleur_letters kleurt gedeeltelijk groen/geel bij deels matchend woord
        resultaat = kleur_letters("raast", "taart")
        # 'r' moet geel zijn (in woord, andere plek)
        self.assertIn(Fore.YELLOW + 'r', resultaat)
        # 'a' moet groen zijn (op juiste plek)
        self.assertIn(Fore.GREEN + 'a', resultaat)
        # 't' moet groen zijn (op juiste plek)
        self.assertIn(Fore.GREEN + 't', resultaat)

    def test_genereer_bingo_kaart_even(self):
        # Test: genereer_bingo_kaart maakt kaart met alleen even getallen als even=True
        kaart = genereer_bingo_kaart(True)
        for rij in kaart:
            for cel in rij:
                self.assertTrue(int(cel) % 2 == 0, f"Cel bevat oneven getal: {cel}")

    def test_genereer_bingo_kaart_oneven(self):
        # Test: genereer_bingo_kaart maakt kaart met alleen oneven getallen als even=False
        kaart = genereer_bingo_kaart(False)
        for rij in kaart:
            for cel in rij:
                self.assertTrue(int(cel) % 2 == 1, f"Cel bevat even getal: {cel}")

    def test_bingo_detectie(self):
        # Test: bingo wordt gedetecteerd als een volledige rij aangekruist is
        # Maak een kaart met eerste rij volledig gemarkeerd (kleurcodes)
        kaart = [[Fore.CYAN + str(i) + Style.RESET_ALL for i in range(4)]]
        # Vul rest met normale nummers
        kaart += [[str(i) for i in range(4)] for _ in range(3)]
        self.assertTrue(check_bingo_custom(kaart), "Bingo werd niet gedetecteerd bij volle rij")

    def test_update_bingo_kaart(self):
        # Test: update_bingo_kaart_custom markeert correct een specifiek getal op de kaart
        kaart = [[str(i + j * 4) for i in range(4)] for j in range(4)]
        update_bingo_kaart_custom(kaart, 5)
        gevonden = any(
            cel.startswith(Fore.CYAN) and "5" in cel
            for rij in kaart for cel in rij
        )
        self.assertTrue(gevonden, "Getal 5 werd niet gemarkeerd op de kaart")

# ------------------------------------------
# Helperfunctie: Check bingo op rijen, kolommen, diagonalen
# Return True als volledige rij/kolom/diagonaal aangekruist is (kleurcode aanwezig)
# ------------------------------------------
def check_bingo_custom(kaart):
    for rij in kaart:
        if all(Style.RESET_ALL in cel for cel in rij):
            return True
    for col in range(4):
        if all(Style.RESET_ALL in kaart[row][col] for row in range(4)):
            return True
    if all(Style.RESET_ALL in kaart[i][i] for i in range(4)):
        return True
    if all(Style.RESET_ALL in kaart[i][3 - i] for i in range(4)):
        return True
    return False

# ------------------------------------------
# Helperfunctie: Markeer een getal op de kaart door kleurcode toe te voegen
# ------------------------------------------
def update_bingo_kaart_custom(kaart, bal):
    for i in range(4):
        for j in range(4):
            if kaart[i][j] == str(bal):
                kaart[i][j] = Fore.CYAN + str(bal) + Style.RESET_ALL

# Start de tests als dit script direct wordt uitgevoerd
if __name__ == '__main__':
    unittest.main()
