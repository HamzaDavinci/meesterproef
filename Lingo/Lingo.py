from colorama import Fore, Style, init
from woorden import kies_woord, woord_splitter
from kleur import kleur_letters
from bingo import genereer_bingo_kaart, update_bingo_kaart, toon_bingo_kaart
from bal import grabbel_bal
from regels import check_win_voorwaarden, check_verlies_voorwaarden

init(autoreset=True)

while True:
    game_running = True
    ronde = 0
    beurt = 1

    team1_score = {"groene_ballen": 0, "rode_ballen": 0, "goed_geraden": 0, "fout_ballen": 0}
    team2_score = {"groene_ballen": 0, "rode_ballen": 0, "goed_geraden": 0, "fout_ballen": 0}

    bingo_kaart_team1 = genereer_bingo_kaart(even=True)
    bingo_kaart_team2 = genereer_bingo_kaart(even=False)

    ballenbak_team1 = [cel for rij in bingo_kaart_team1 for cel in rij] + ["groen", "rood"] * 3
    ballenbak_team2 = [cel for rij in bingo_kaart_team2 for cel in rij] + ["groen", "rood"] * 3

    print('Welkom bij Lingo')
    team1 = input('Hallo Team 1, wat is jullie teamnaam? ').lower()
    team2 = input('Hallo Team 2, wat is jullie teamnaam? ').lower()

    while game_running:
        ronde += 1
        woord = kies_woord()
        split_word = woord_splitter(woord)

        print(f'\nRonde {ronde}')
        print(f'DEBUG: Het woord is "{woord}".')
        print(f'De eerste letter is: {Fore.GREEN + split_word[0] + Fore.RESET} _ _ _ _')

        huidig_team = team1 if beurt == 1 else team2
        huidig_score = team1_score if beurt == 1 else team2_score
        huidig_kaart = bingo_kaart_team1 if beurt == 1 else bingo_kaart_team2
        huidig_ballenbak = ballenbak_team1 if beurt == 1 else ballenbak_team2

        for poging in range(5):
            raden = input(f'\nPoging {poging + 1} voor {huidig_team}: ').lower()
            if len(raden) != 5:
                print(Fore.RED + "Het woord moet precies 5 letters lang zijn. Probeer opnieuw.")
                continue

            if raden == woord:
                print(Fore.GREEN + 'Gefeliciteerd! Je hebt het woord geraden!')
                huidig_score["goed_geraden"] += 1
                huidig_score["fout_ballen"] = 0

                aantal_grabbels = 2
                while aantal_grabbels > 0:
                    bal = grabbel_bal(huidig_team, huidig_ballenbak)
                    if bal is None:
                        game_running = False
                        break
                    if bal == "groen":
                        huidig_score["groene_ballen"] += 1
                        print(Fore.GREEN + f"{huidig_team} heeft een {bal} bal getrokken.")
                    elif bal == "rood":
                        huidig_score["rode_ballen"] += 1
                        print(Fore.RED + f"{huidig_team} heeft een {bal} bal getrokken.")
                        break
                    else:
                        update_bingo_kaart(huidig_kaart, bal)
                        print(f"{huidig_team} heeft een {bal} bal getrokken.")
                    aantal_grabbels -= 1

                toon_bingo_kaart(huidig_team, huidig_kaart)

                if check_win_voorwaarden(huidig_team, huidig_score, huidig_kaart) or check_verlies_voorwaarden(huidig_team, huidig_score):
                    game_running = False
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
