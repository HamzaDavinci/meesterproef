import random
from colorama import Fore, Style, init
from lingowords import words  # Importeer de woordenlijst

# Initialiseer colorama
init(autoreset=True)

while True:
    # Globale variabelen
    game_running = True
    ronde = 0
    beurt = 1  # 1 voor Team 1, 2 voor Team 2

    # Score bijhouden
    team1_score = {
        "groene_ballen": 0,
        "rode_ballen": 0,
        "goed_geraden": 0,
        "fout_ballen": 0
    }
    team2_score = {
        "groene_ballen": 0,
        "rode_ballen": 0,
        "goed_geraden": 0,
        "fout_ballen": 0
    }

    # Bingo-kaarten genereren met even of oneven nummers
    def genereer_bingo_kaart(even=True):
        if even:
            # random.sample(...) pakt een paar willekeurige getallen uit een lijst, zonder dubbele
            # Bijvoorbeeld: random.sample([2, 4, 6, 8], 2) → [4, 8]
            nummers = random.sample([i for i in range(2, 100, 2)], 16)  # genoeg even getallen (pakt 16 getallen)
        else:
            nummers = random.sample([i for i in range(1, 100, 2)], 16)  # genoeg oneven getallen
        kaart = []
        for i in range(4):
            rij = []
            for j in range(4):
                nummer = nummers[i * 4 + j]
                rij.append(str(nummer))
            kaart.append(rij)
        return kaart

    # als je de even aanpast verander je de lijst van ballen in de bingo lijst:
    bingo_kaart_team1 = genereer_bingo_kaart(even=True)
    bingo_kaart_team2 = genereer_bingo_kaart(even=False)

    # Ballenbakken voor de twee teams
    ballenbak_team1 = []
    ballenbak_team2 = []

    # Voeg ballen toe voor team 1 en team 2, afhankelijk van hun bingo-kaarten
    for i in range(4):
        for j in range(4):
            ballenbak_team1.append(bingo_kaart_team1[i][j])
            ballenbak_team2.append(bingo_kaart_team2[i][j])

    # Voeg 3 groene en 3 rode ballen toe voor beide teams
    for _ in range(3):
        ballenbak_team1.append("groen")
        ballenbak_team1.append("rood")
        ballenbak_team2.append("groen")
        ballenbak_team2.append("rood")

    print('Welkom bij Lingo')

    team1 = input('Hallo Team 1, wat is jullie teamnaam? ').lower()
    team2 = input('Hallo Team 2, wat is jullie teamnaam? ').lower()

    # Functie om een woord te splitsen in letters
    def woord_splitter(woord):
        gesplitst = []
        for letter in woord:
            gesplitst.append(letter)
        return gesplitst

    # Functie om de letters van het geraden woord te kleuren
    def kleur_letters(geraden_woord, correct_woord):
        correct_woord_lijst = []
        for letter in correct_woord:
            correct_woord_lijst.append(letter)

        geraden_woord_lijst = []
        for letter in geraden_woord:
            geraden_woord_lijst.append(letter)

        gekleurd_woord = []

        # Eerste pass: markeer juiste letters op de juiste plek (groen)
        for i in range(len(geraden_woord_lijst)):
            letter_geraden = geraden_woord_lijst[i]
            letter_correct = correct_woord_lijst[i]

            if letter_geraden == letter_correct:
                gekleurd_woord.append(Fore.GREEN + letter_geraden)
                geraden_woord_lijst[i] = None
                correct_woord_lijst[i] = None
            else:
                gekleurd_woord.append(Fore.RESET + letter_geraden)

        # Tweede pass: markeer juiste letters op de verkeerde plek (geel)
        for i in range(len(geraden_woord_lijst)):
            letter_geraden = geraden_woord_lijst[i]

            if letter_geraden is not None and letter_geraden in correct_woord_lijst:
                index_in_correct = correct_woord_lijst.index(letter_geraden)
                if correct_woord_lijst[index_in_correct] is not None:
                    gekleurd_woord[i] = Fore.YELLOW + letter_geraden
                    correct_woord_lijst[index_in_correct] = None

        resultaat = ''
        for letter in gekleurd_woord:
            resultaat += letter
        return resultaat

    # Functie om een bal te trekken voor een team
    def grabbel_bal(team):
        if team == team1:
            if len(ballenbak_team1) == 0:
                print(Fore.RED + "De ballenbak van Team 1 is leeg! Het spel is afgelopen.")
                return None
            gekozen_index = random.randint(0, len(ballenbak_team1) - 1)
            bal = ballenbak_team1[gekozen_index]
            del ballenbak_team1[gekozen_index]
            return bal
        elif team == team2:
            if len(ballenbak_team2) == 0:
                print(Fore.RED + "De ballenbak van Team 2 is leeg! Het spel is afgelopen.")
                return None
            gekozen_index = random.randint(0, len(ballenbak_team2) - 1)
            bal = ballenbak_team2[gekozen_index]
            del ballenbak_team2[gekozen_index]
            return bal

    # Functie om de bingo-kaart van een team bij te werken na het trekken van een bal
    def update_bingo_kaart(team, bal):
        if team == team1:
            kaart = bingo_kaart_team1
        else:
            kaart = bingo_kaart_team2

        for i in range(4):
            for j in range(4):
                if kaart[i][j] == str(bal):
                    kaart[i][j] = Fore.CYAN + str(bal) + Style.RESET_ALL

    # Functie om te controleren of er bingo is
    def check_bingo(team):
        if team == team1:
            kaart = bingo_kaart_team1
        else:
            kaart = bingo_kaart_team2

        # Check rijen
        for rij in kaart:
            bingo = True
            for cel in rij:
                if cel is None or not isinstance(cel, str) or Style.RESET_ALL not in cel:
                    bingo = False
                    break
            if bingo:
                return True

        # Check kolommen
        for kolom in range(4):
            bingo = True
            for rij in range(4):
                cel = kaart[rij][kolom]
                if cel is None or not isinstance(cel, str) or Style.RESET_ALL not in cel:
                    bingo = False
                    break
            if bingo:
                return True

        # Check diagonalen
        diagonaal1 = True
        diagonaal2 = True
        for i in range(4):
            if kaart[i][i] is None or Style.RESET_ALL not in kaart[i][i]:
                diagonaal1 = False
            if kaart[i][3 - i] is None or Style.RESET_ALL not in kaart[i][3 - i]:
                diagonaal2 = False
        if diagonaal1 or diagonaal2:
            return True

        return False

    # Functie om de winvoorwaarden te controleren
    def check_win_voorwaarden(team, score):
        if score["groene_ballen"] >= 3:
            print(Fore.GREEN + f"{team} heeft 3 groene ballen getrokken en wint het spel!")
            return True
        if check_bingo(team):
            print(Fore.GREEN + f"{team} heeft een lijn op de bingo-kaart en wint het spel!")
            return True
        if score["goed_geraden"] >= 10:
            print(Fore.GREEN + f"{team} heeft 10 woorden goed geraden en wint het spel!")
            return True
        return False

    # Functie om de verliesvoorwaarden te controleren
    def check_verlies_voorwaarden(team, score):
        if score["rode_ballen"] >= 3:
            print(Fore.RED + f"{team} heeft 3 rode ballen getrokken en verliest het spel!")
            return True
        if score["fout_ballen"] >= 3:
            print(Fore.RED + f"{team} heeft 3 woorden op rij fout geraden en verliest het spel!")
            return True
        return False

    # Functie om de bingo-kaart van een team te tonen
    def toon_bingo_kaart(team):
        if team == team1:
            kaart = bingo_kaart_team1
        else:
            kaart = bingo_kaart_team2

        print(f"\nBingo-kaart voor {team}:")
        for rij in kaart:
            regel = ""
            for cel in rij:
                if cel is not None:
                    regel += cel + " | "
                else:
                    regel += " " + " | "
            print(regel.strip(" | "))
            
    # Spel loop
    while game_running:
        ronde += 1
        woord = random.choice(words)
        split_word = woord_splitter(woord)
        print(f'\nRonde {ronde}')
        print(f'DEBUG: Het woord is "{woord}".')
        print(f'De eerste letter is: {Fore.GREEN + split_word[0] + Fore.RESET} _ _ _ _')

        huidig_team = team1 if beurt == 1 else team2
        huidig_score = team1_score if beurt == 1 else team2_score

        for poging in range(5):
            while True:
                print(f'\nPoging {poging + 1} voor {huidig_team}:')
                raden = input('Raad het woord: ').lower()
                if len(raden) == 5:
                    break
                print(Fore.RED + "Het woord moet precies 5 letters lang zijn. Probeer opnieuw.")

            if raden == woord:
                print(Fore.GREEN + 'Gefeliciteerd! Je hebt het woord geraden!')
                huidig_score["goed_geraden"] += 1
                huidig_score["fout_ballen"] = 0

                aantal_grabbels = 2
                while aantal_grabbels > 0:
                    bal = grabbel_bal(huidig_team)
                    if bal is None:
                        game_running = False
                        break
                    if bal == "groen":
                        huidig_score["groene_ballen"] += 1
                        print(Fore.GREEN + f"{huidig_team} heeft een {bal} bal getrokken.")
                    elif bal == "rood":
                        huidig_score["rode_ballen"] += 1
                        print(Fore.RED + f"{huidig_team} heeft een {bal} bal getrokken.")
                        break  # Geen tweede grabbel na rood
                    else:
                        update_bingo_kaart(huidig_team, bal)
                        print(f"{huidig_team} heeft een {bal} bal getrokken.")
                    aantal_grabbels -= 1


                toon_bingo_kaart(huidig_team)

                if check_win_voorwaarden(huidig_team, huidig_score) or check_verlies_voorwaarden(huidig_team, huidig_score):
                    game_running = False
                    break

                beurt = 2 if beurt == 1 else 1
                break
            else:
                print(kleur_letters(raden, woord))
        else:
            print(Fore.RED + 'Helaas, je hebt het woord niet geraden.')
            huidig_score["fout_ballen"] += 1
            if check_verlies_voorwaarden(huidig_team, huidig_score):
                game_running = False
            beurt = 2 if beurt == 1 else 1

    print('Bedankt voor het spelen!')

    opnieuw = input('Wil je nog een keer spelen? (ja/nee): ').lower()
    if opnieuw != 'ja':
        print('Tot de volgende keer!')
        break
