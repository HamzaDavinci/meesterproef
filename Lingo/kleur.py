from colorama import Fore, Style

def kleur_letters(geraden_woord, correct_woord):
    correct_woord_lijst = list(correct_woord)
    geraden_woord_lijst = list(geraden_woord)

    gekleurd_woord = []

    for i in range(len(geraden_woord_lijst)):
        letter_geraden = geraden_woord_lijst[i]
        letter_correct = correct_woord_lijst[i]

        if letter_geraden == letter_correct:
            gekleurd_woord.append(Fore.GREEN + letter_geraden)
            geraden_woord_lijst[i] = None
            correct_woord_lijst[i] = None
        else:
            gekleurd_woord.append(Fore.RESET + letter_geraden)

    for i in range(len(geraden_woord_lijst)):
        letter_geraden = geraden_woord_lijst[i]

        if letter_geraden is not None and letter_geraden in correct_woord_lijst:
            index_in_correct = correct_woord_lijst.index(letter_geraden)
            if correct_woord_lijst[index_in_correct] is not None:
                gekleurd_woord[i] = Fore.YELLOW + letter_geraden
                correct_woord_lijst[index_in_correct] = None

    return ''.join(gekleurd_woord)
